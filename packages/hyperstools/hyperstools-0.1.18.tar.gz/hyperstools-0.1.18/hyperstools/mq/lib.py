# encoding: utf-8
import json
import logging
import pickle
from traceback import format_exc

import pika
from django.conf import settings
from django.db import close_old_connections

LOGGER = logging.getLogger("tools")


class Consumer(object):
    """This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    """

    EXCHANGE_TYPE = "direct"

    def __init__(self, identify, callback, logger=None):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        :param str amqp_url: The AMQP url to connect with

        """
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._callback = callback
        self.identify = identify
        self.QUEUE = identify.pop("queue", "")
        self.EXCHANGE = identify.pop("exchange", "")
        self.ROUTING_KEY = identify.pop("routing_key", "")
        self.LOGGER = logger or LOGGER

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """
        identify = self.identify
        credentials = pika.PlainCredentials(
            identify["user"], identify["password"]
        )

        parameters = pika.ConnectionParameters(
            identify["host"], identify["port"], identify["vhost"], credentials, heartbeat=30 * 60
        )
        return pika.SelectConnection(
            parameters, self.on_connection_open, stop_ioloop_on_close=False
        )

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        data = None
        self.LOGGER.info(
            "Received message # %s from %s: %s",
            basic_deliver.delivery_tag,
            properties.app_id,
            body,
        )
        try:
            data = json.loads(body)
        except Exception:
            try:
                data = pickle.loads(body)
            except Exception:
                self.LOGGER.error(format_exc())
                return unused_channel.basic_ack(
                    delivery_tag=basic_deliver.delivery_tag
                )
        close_old_connections()
        try:
            self._callback(data)
        except Exception:
            self.LOGGER.error(format_exc())
        return unused_channel.basic_ack(
            delivery_tag=basic_deliver.delivery_tag
        )

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        self.LOGGER.info("Connection opened")
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        self.LOGGER.info("Adding connection close callback")
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.LOGGER.warning(
                "Connection closed, reopening in 5 seconds: (%s) %s",
                reply_code,
                reply_text,
            )
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:

            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        self.LOGGER.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        self.LOGGER.info("Channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        self.LOGGER.info("Adding channel close callback")
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self.LOGGER.warning(
            "Channel %i was closed: (%s) %s", channel, reply_code, reply_text
        )
        self._connection.close()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        self.LOGGER.info("Declaring exchange %s", exchange_name)
        self._channel.exchange_declare(
            self.on_exchange_declareok,
            exchange_name,
            self.EXCHANGE_TYPE,
            durable=True,
        )

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        self.LOGGER.info("Exchange declared")
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        self.LOGGER.info("Declaring queue %s", queue_name)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.queue_declare(
            self.on_queue_declareok, queue_name, durable=True
        )

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self.LOGGER.info(
            "Binding %s to %s with %s",
            self.EXCHANGE,
            self.QUEUE,
            self.ROUTING_KEY,
        )
        self._channel.queue_bind(
            self.on_bindok, self.QUEUE, self.EXCHANGE, self.ROUTING_KEY
        )

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        self.LOGGER.info("Queue bound")
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        self.LOGGER.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.on_message, self.QUEUE
        )

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        self.LOGGER.info("Adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        self.LOGGER.info(
            "Consumer was cancelled remotely, shutting down: %r", method_frame
        )
        if self._channel:
            self._channel.close()

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        self.LOGGER.info("Acknowledging message %s", delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            self.LOGGER.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        self.LOGGER.info(
            "RabbitMQ acknowledged the cancellation of the consumer"
        )
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        self.LOGGER.info("Closing the channel")
        self._channel.close()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        self.LOGGER.info("Stopping")
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()
        self.LOGGER.info("Stopped")

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        self.LOGGER.info("Closing connection")
        self._connection.close()


class Publisher(object):
    """This is an example publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    It uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.

    """

    EXCHANGE_TYPE = "direct"
    PUBLISH_INTERVAL = 1

    def __init__(
        self, identify: dict, message: dict, encoder: str, logger=None
    ):
        """Setup the example publisher object, passing in the URL we will use
        to connect to RabbitMQ.

        :param str amqp_url: The URL for connecting to RabbitMQ

        """
        self._connection = None
        self._channel = None

        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = 0
        self._message = message

        self._encoder = encoder
        self._stopping = False
        self.identify = identify
        self.QUEUE = identify.pop("queue", "")
        self.EXCHANGE = identify.pop("exchange", "")
        self.ROUTING_KEY = identify.pop("routing_key", "")
        self.LOGGER = logger or LOGGER

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika. If you want the reconnection to work, make
        sure you set stop_ioloop_on_close to False, which is not the default
        behavior of this adapter.

        :rtype: pika.SelectConnection

        """
        identify = self.identify
        self.LOGGER.info("Connecting to %s", identify)
        credentials = pika.PlainCredentials(
            identify["user"], identify["password"]
        )
        parameters = pika.ConnectionParameters(
            identify["host"], identify["port"], identify["vhost"], credentials
        )
        return pika.SelectConnection(
            parameters,
            on_open_callback=self.on_connection_open,
            on_close_callback=self.on_connection_closed,
            stop_ioloop_on_close=False,
        )

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        self.LOGGER.info("Connection opened")
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            self.LOGGER.warning(
                "Connection closed, reopening in 5 seconds: (%s) %s",
                reply_code,
                reply_text,
            )
            self._connection.add_timeout(5, self._connection.ioloop.stop)

    def open_channel(self):
        """This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.

        """
        self.LOGGER.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        self.LOGGER.info("Channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        self.LOGGER.info("Adding channel close callback")
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self.LOGGER.warning(
            "Channel was closed: (%s) %s", reply_code, reply_text
        )
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        self.LOGGER.info("Declaring exchange %s", exchange_name)
        self._channel.exchange_declare(
            self.on_exchange_declareok,
            exchange_name,
            self.EXCHANGE_TYPE,
            durable=True,
        )

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        self.LOGGER.info("Exchange declared")
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        self.LOGGER.info("Declaring queue %s", queue_name)
        self._channel.queue_declare(
            self.on_queue_declareok, queue_name, durable=True
        )

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self.LOGGER.info(
            "Binding %s to %s with %s",
            self.EXCHANGE,
            self.QUEUE,
            self.ROUTING_KEY,
        )
        self._channel.queue_bind(
            self.on_bindok, self.QUEUE, self.EXCHANGE, self.ROUTING_KEY
        )

    def on_bindok(self, unused_frame):
        """This method is invoked by pika when it receives the Queue.BindOk
        response from RabbitMQ. Since we know we're now setup and bound, it's
        time to start publishing."""
        self.LOGGER.info("Queue bound")
        self.start_publishing()

    def start_publishing(self):
        """This method will enable delivery confirmations and schedule the
        first message to be sent to RabbitMQ

        """
        self.LOGGER.info("Issuing consumer related RPC commands")
        self.enable_delivery_confirmations()
        self.schedule_next_message()

    def enable_delivery_confirmations(self):
        """Send the Confirm.Select RPC method to RabbitMQ to enable delivery
        confirmations on the channel. The only way to turn this off is to close
        the channel and create a new one.

        When the message is confirmed from RabbitMQ, the
        on_delivery_confirmation method will be invoked passing in a Basic.Ack
        or Basic.Nack method from RabbitMQ that will indicate which messages it
        is confirming or rejecting.

        """
        self.LOGGER.info("Issuing Confirm.Select RPC command")
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """
        confirmation_type = method_frame.method.NAME.split(".")[1].lower()
        self.LOGGER.info(
            "Received %s for delivery tag: %i",
            confirmation_type,
            method_frame.method.delivery_tag,
        )

    def schedule_next_message(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds.

        """
        self.LOGGER.info(
            "Scheduling next message for %0.1f seconds", self.PUBLISH_INTERVAL
        )
        self._connection.add_timeout(
            self.PUBLISH_INTERVAL, self.publish_message
        )

    def publish_message(self):
        """If the class is not stopping, publish a message to RabbitMQ,
        appending a list of deliveries with the message number that was sent.
        This list will be used to check for delivery confirmations in the
        on_delivery_confirmations method.

        Once the message has been sent, schedule another message to be sent.
        The main reason I put scheduling in was just so you can get a good idea
        of how the process is flowing by slowing down and speeding up the
        delivery intervals by changing the PUBLISH_INTERVAL constant in the
        class.

        """
        if self._channel is None or not self._channel.is_open:
            return

        properties = pika.BasicProperties(delivery_mode=2)
        if self._encoder == "pickle":
            message = pickle.dumps(self._message)
        else:
            message = json.dumps(self._message, ensure_ascii=False)

        self.LOGGER.info(f"publish message {self._message}")
        self._channel.basic_publish(
            self.EXCHANGE, self.ROUTING_KEY, message, properties
        )
        self.stop()

    def run(self):
        """Run the example code by connecting and then starting the IOLoop.

        """
        while not self._stopping:
            self._connection = None
            self._deliveries = []
            self._acked = 0
            self._nacked = 0
            self._message_number = 0

            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
            except KeyboardInterrupt:
                self.stop()
                if (
                    self._connection is not None
                    and not self._connection.is_closed
                ):
                    # Finish closing
                    self._connection.ioloop.start()

        self.LOGGER.info("Stopped")

    def stop(self):
        """Stop the example by closing the channel and connection. We
        set a flag here so that we stop scheduling new messages to be
        published. The IOLoop is started because this method is
        invoked by the Try/Catch below when KeyboardInterrupt is caught.
        Starting the IOLoop again will allow the publisher to cleanly
        disconnect from RabbitMQ.

        """
        self.LOGGER.info("Stopping")
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        """Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.

        """
        if self._channel is not None:
            self.LOGGER.info("Closing the channel")
            self._channel.close()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        if self._connection is not None:
            self.LOGGER.info("Closing connection")
            self._connection.close()


class Queue(object):
    def __init__(self, identify: dict, logger=None):
        """初始化rabbitmq的认证信息
        如果identify不存在host、port等key时，则从settings.RABBITMQ中取默认值

        :identify: dict: 认证信息， 如 {'user': 'xxx', 'password': 'xxx', 'queue': 'xxx'}
        :returns: None

        """
        identify.setdefault("host", settings.RABBITMQ["host"])
        identify.setdefault("port", settings.RABBITMQ["port"])
        identify.setdefault("user", settings.RABBITMQ["user"])
        identify.setdefault("password", settings.RABBITMQ["password"])
        identify.setdefault("vhost", settings.RABBITMQ["vhost"])
        identify.setdefault(
            "exchange", settings.RABBITMQ.get("exchange", identify["queue"])
        )
        identify.setdefault(
            "routing_key",
            settings.RABBITMQ.get("routing_key", identify["queue"]),
        )
        self._identify = dict(identify)
        self._connection = None
        self._logger = logger

    def publish(self, message: dict, encoder: str = "json"):
        """发布消息的处理函数
        用法
        with Queue(settings.RABBITMQ) as queue:
            queue.publish({'a': 'b'})

        :message: dict: 消息体
        :returns: None

        """
        pub = Publisher(
            self._identify, message, encoder=encoder, logger=self._logger
        )
        pub._connection = pub.connect()
        pub._connection.ioloop.start()
        self._connection = pub

    def listen(self, callback):
        consumer = Consumer(self._identify, callback, logger=self._logger)
        consumer.run()

    def __call__(self, callback):
        """注册listen的回调函数
        在调用callback函数之前，会先尝试使用json.loads 解析消息
        然后尝试使用pickle.loads 解析消息，
        如果解析消息失败，则直接返回ack,
        解析成功后会调用
        close_old_connections, 再调用callback函数
        其中回调消息会经过异常处理

        用法

        @Queue(settings.RABBITMQ)
        def listen(body: dict):
            pass

        listen()

        :callback: 消费者的回调函数
        :returns: None

        """

        def inner():
            return self.listen(callback)

        return inner

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
