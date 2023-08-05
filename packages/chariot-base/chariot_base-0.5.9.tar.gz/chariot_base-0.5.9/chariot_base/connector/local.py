#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import gmqtt
from ..utilities import Tracer


class LocalConnector(object):
    """
    All subscribers/publisers at Chariot project should extend this class
    """
    def __init__(self):
        self.connack = None
        self.client = None
        self.tracer = None

        self.disconnected = False
        self.connected = False

    def clear(self):
        self.__init__()

    def subscribe(self, topic, qos=1):
        """
        Subscribe to a topic
        
        :param topic: Which topic the subscriber should listen for new message.
        :param qos: MQTT broker quality of service
        """
        self.client.subscribe(topic, qos=qos)

    def publish(self, topic, msg, qos=1):
        """
        Publish to a topic

        :param msg: the published message
        :param qos: MQTT broker quality of service
        """
        self.client.publish(topic, msg, qos=qos)

    def on_message(self, client, topic, payload, qos, properties):
        """
        Handler for new message

        :param client: the subscribed MQTT client
        :param topic: the MQTT topic
        :param payload: the message 
        :param qos: MQTT broker quality of service
        :param properties: Custom properties
        """
        pass

    def on_subscribe(self, client, mid, qos):
        """
        The handler run when the client subscribed to a new topic

        :param client: the subscribed MQTT client
        :param mid:
        :param qos: MQTT broker quality of service
        """
        pass

    def on_disconnect(self, client, packet):
        """
        The handler run when the connections is fineshed

        :param client: the subscribed MQTT client
        :param packet:
        """
        self.disconnected = True

    def on_connect(self, client, flags, rc, properties):
        """
        The handler run when the connections is established

        :param client: the subscribed MQTT client
        :param flags:
        :param rc:
        :param properties: Custom properties
        """
        self.connected = True
        self.connack = (flags, rc, properties)

    def register_for_client(self, client):
        """
        Register handlers to the client.

        :param client: Client to register handlers
        """
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe

        self.client = client

    def inject_tracer(self, tracer):
        """
        Inject an opentracing client

        :param tracer: the opentracing client 
        """
        self.tracer = tracer

    def set_up_tracer(self, options):
        """
        Configure a new opentracing client

        :param options: options to configure the new client
        """
        self.tracer = Tracer(options)
        self.tracer.init_tracer()

    def start_span(self, id, child_span=None):
        """
        Start a new logging span

        :param id: identifier of a new logging span
        :param child_span: parent span
        """
        if self.tracer is None:
            return

        if child_span is None:
            return self.tracer.tracer.start_span(id)
        else:
            return self.tracer.tracer.start_span(id, child_of=child_span)

    def close_span(self, span):
        """
        Close a logging span
        
        :param span: Span to close
        """
        if self.tracer is None:
            return
        span.finish()


async def create_client(options, postfix='_client'):
    """
    Create a new GMQTT client

    :param options: Options for client initialization
    :para postfix: Unique postfix for the client
    """
    client_id = '%s%s' % (uuid.uuid4(), postfix)
  
    client = gmqtt.Client(client_id, clean_session=True)
    await client.connect(host=options['host'], port=options['port'], version=4)

    return client