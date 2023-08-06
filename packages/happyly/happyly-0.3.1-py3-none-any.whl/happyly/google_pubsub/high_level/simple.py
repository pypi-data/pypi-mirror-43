from typing import Union, Optional

import marshmallow

from happyly.handling.dummy_handler import DUMMY_HANDLER
from happyly.google_pubsub.deserializers import JSONDeserializerWithRequestIdRequired
from happyly.google_pubsub.publishers import GooglePubSubPublisher
from happyly.google_pubsub.serializers import BinaryJSONSerializer
from happyly.google_pubsub.subscribers import GooglePubSubSubscriber
from happyly.handling import Handler
from happyly.listening import Listener
from happyly.listening.executor import Executor


class GoogleSimpleSender(
    Executor[Union[None, JSONDeserializerWithRequestIdRequired], GooglePubSubPublisher]
):
    def __init__(
        self,
        output_schema: marshmallow.Schema,
        to_topic: str,
        project: str,
        handler: Handler = DUMMY_HANDLER,
        input_schema: Optional[marshmallow.Schema] = None,
    ):
        if input_schema is None:
            deserializer = None
        else:
            deserializer = JSONDeserializerWithRequestIdRequired(schema=input_schema)
        publisher = GooglePubSubPublisher(
            project=project,
            publish_all_to=to_topic,
            serializer=BinaryJSONSerializer(schema=output_schema),
        )
        super().__init__(
            publisher=publisher, handler=handler, deserializer=deserializer
        )


class GoogleSimpleReceiver(Listener[JSONDeserializerWithRequestIdRequired, None]):
    def __init__(
        self,
        input_schema: marshmallow.Schema,
        from_subscription: str,
        project: str,
        handler: Handler,
    ):
        subscriber = GooglePubSubSubscriber(
            project=project, subscription_name=from_subscription
        )
        deserializer = JSONDeserializerWithRequestIdRequired(schema=input_schema)
        super().__init__(
            subscriber=subscriber, handler=handler, deserializer=deserializer
        )


class GoogleSimpleReceiveAndReply(
    Listener[JSONDeserializerWithRequestIdRequired, GooglePubSubPublisher]
):
    def __init__(
        self,
        handler: Handler,
        input_schema: marshmallow.Schema,
        from_subscription: str,
        output_schema: marshmallow.Schema,
        to_topic: str,
        project: str,
    ):
        subscriber = GooglePubSubSubscriber(
            project=project, subscription_name=from_subscription
        )
        deserializer = JSONDeserializerWithRequestIdRequired(schema=input_schema)
        publisher = GooglePubSubPublisher(
            project=project,
            publish_all_to=to_topic,
            serializer=BinaryJSONSerializer(schema=output_schema),
        )
        super().__init__(
            handler=handler,
            deserializer=deserializer,
            subscriber=subscriber,
            publisher=publisher,
        )


# for compatibility
GoogleReceiveAndReplyComponent = GoogleSimpleReceiveAndReply
