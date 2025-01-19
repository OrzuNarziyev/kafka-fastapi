import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def publish(topic: str, key: str, data: dict):
    r = producer.send(topic, key=key.encode('utf-8'), value=data)
    producer.flush()
    return r.is_done
