from kafka import KafkaConsumer
import json


def get_kafka_consumer(topic: str, bootstrap_servers: str = "kafka:9092"):
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )


def kafka_generator(topic: str = 'notifications', bootstrap_servers: str = "kafka:9092"):
    consumer = get_kafka_consumer(topic, bootstrap_servers)
    for message in consumer:
        yield message.value.decode("utf-8")

