import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
import contextlib
from sse_starlette.sse import EventSourceResponse

import sys
import six

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from app.consumer import *
from app.producer import publish

CLIENT_ID = 'fastapi-client'
KAFKA_TOPIC = 'notifications'


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:9092',
        client_id='fastapi-client',
    )
    if not KAFKA_TOPIC and admin_client.list_topics():
        admin_client.create_topics(
            new_topics=[
                NewTopic(
                    name=KAFKA_TOPIC,
                    num_partitions=1,
                    replication_factor=1,
                )
            ], validate_only=False
        )
    yield


app = FastAPI(lifespan=lifespan)


class Message(BaseModel):
    event: str
    data: dict


@app.post("/send")
async def send(message: Message):
    result = publish('notifications', 'key', data=message.model_dump())
    return {
        'publish': result,
    }


@app.get("/stream")
async def stream(request: Request):
    consumer = get_kafka_consumer('notifications')

    async def event_stream():
        while True:
            if await request.is_disconnected():
                break
            message = consumer.poll()
            if not len(message) == 0:
                for key, value in message.items():
                    for record in value:
                        yield record.value

            await asyncio.sleep(1)

    return EventSourceResponse(event_stream())
