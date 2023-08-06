import time
import threading
from clitellum import errorGateway
from clitellum.core import serialization, loggerManager
from clitellum.core.bus import MessageBuilder
from clitellum.core.fsm import Startable
from clitellum.endpoints import gateways
from clitellum.endpoints.gateways import SenderGateway, ReceiverGateway
from clitellum.core.monitoring import Monitoring
import base64

__author__ = 'Sergio'


'''
@package clitellum.processors
Este paquete contiene las clases que encapsulan la relacion del los mensajes con sus manejadores
'''


class Bus:
    '''
    Clase que representa la interfaz para poder comunicar con el BUS
    '''
    def __init__(self):
        pass

    @property
    def identification(self):
        return None

    def send(self, message, key, header=None):
        pass

    def reply(self, message, key, header=None):
        pass



class AgentProcessor(Startable, Bus):
    '''
    Clase que implementa el procesamiento de los mensajes
    '''
    def __init__(self, identification, receiver_gateway, sender_gateway, error_gateway=None):
        Startable.__init__(self)
        Bus.__init__(self)
        self._receiver_gateway = receiver_gateway
        self._senderGateway = sender_gateway
        self._identification = identification
        self._receiver_gateway.OnMessageReceived.add(self.__on_message_received)
        self._handler_manager = None
        self._error_gateway = error_gateway
        self._reply_sender = None
        self._reply_receiver = None
        self._monitoring = None
        self._heartbeat_th = threading.Thread(target=self._heartbeat_process)

    @property
    def identification(self):
        return self._identification

    def set_reply_sender(self, sender_gateway: SenderGateway):
        self._reply_sender = sender_gateway

    def set_reply_receiver(self, receiver_gateway: ReceiverGateway):
        self._reply_receiver = receiver_gateway
        self._reply_receiver.OnMessageReceived.add(self.__on_message_received)

    def set_monitoring(self, monitoring: Monitoring):
        self._monitoring = monitoring

    def configure(self, handler_manager):
        self._handler_manager = handler_manager

    def __on_message_received(self, sender, args):
        try:
            message_bus = serialization.loads(args.message)

            handler = self._handler_manager.get_handler(message_bus['Header']['BodyType'])
            if self._monitoring is not None:
                self._monitoring.message_recieved(self._identification, message_bus['Header']['BodyType'], len(args.message))

            handler.initialize(self, message_bus['Header'])

            body_str = base64.b64decode(message_bus['Body'].encode('utf-8')).decode('utf-8')
            body = serialization.loads(body_str)

            handler.handle_message(body)

        except Exception as ex:
            loggerManager.get_processors_logger().exception("Error al procesar el mensaje %s", args.message)
            self._send_error(args.message, ex)

    def _invokeOnStart(self):
        Startable._invokeOnStart(self)
        self._receiver_gateway.start()
        self._senderGateway.connect()
        if self._error_gateway is not None:
            self._error_gateway.connect()
        
        if self._reply_sender is not None:
            self._reply_sender.connect()
        
        if self._reply_receiver is not None:
            self._reply_receiver.start()
        
        if self._monitoring is not None:
            self._heartbeat_th.start()

    def _invokeOnStopped(self):
        Startable._invokeOnStopped(self)
        self._receiver_gateway.stop()
        self._senderGateway.close()
        if self._error_gateway is not None:
            self._error_gateway.close()

        if self._reply_sender is not None:
            self._reply_sender.close()
        
        if self._reply_receiver is not None:
            self._reply_receiver.stop()

        if self._monitoring is not None:
            self._heartbeat_th.join()

    def _heartbeat_process(self):
        while self.state == Startable.RUNNING:
            self._monitoring.send_heartbeat(self._identification)
            time.sleep(10)


    def send(self, message, key, header=None):
 
        body_str = serialization.dumps(message)
        body_encode = base64.b64encode(body_str.encode('utf-8')).decode('utf-8')

        message_bus = MessageBuilder.create() \
                      .set_service(self.identification) \
                      .set_type(key) \
                      .set_body(body_encode) \
                      .set_context(header) \
                      .build()

        message_str = serialization.dumps(message_bus)
        self._senderGateway.send(message_str, key)

    def reply(self, message, key, header=None):        
        reply_service = header['CallStack'].pop()

        body_str = serialization.dumps(message)
        body_encode = base64.b64encode(body_str.encode('utf-8')).decode('utf-8')

        message_bus = MessageBuilder.create() \
                      .set_service(self.identification) \
                      .set_type(key) \
                      .set_body(body_encode) \
                      .set_context(header) \
                      .set_reply() \
                      .build()

        message_str = serialization.dumps(message_bus)
        if self._reply_sender is None:
            self._senderGateway.send(message_str, key)
        else:
            self._reply_sender.send(message_str, reply_service['ReplyKey'])


    def _send_error(self, message_received, exception):
        if self._error_gateway is None:
            return
        message = errorGateway.create_error_message(message_received, exception)
        message_bus = MessageBuilder.create() \
                      .set_service(self.identification) \
                      .set_type('Error.ErrorHandler') \
                      .set_body(message) \
                      .build()

        message_str = serialization.dumps(message_bus)
        self._error_gateway.send(message_str, "Error.ErrorHandler")

    def __del__(self):
        Startable.__del__(self)
