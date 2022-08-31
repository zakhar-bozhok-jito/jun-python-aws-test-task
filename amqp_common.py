from asyncio.log import logger
from dataclasses import dataclass
import os
import time
import pika

def createConnectionToAMQP(host, port, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    return (connection, channel)

def retryingConnectionToAMQP(host, port, queue_name):
    for i in range(10):
        try:
            return createConnectionToAMQP(host, port, queue_name)
        except Exception:
            time.sleep(5)
    raise Exception("Could not connect to AMQP")

@dataclass
class AMQPConfig:
    def __init__(self, host: str, port: int, queue_name: str):
        self.host = host
        self.port = port
        self.queue_name = queue_name
    
    @staticmethod
    def fromENV():
        return AMQPConfig(
            os.environ.get("AMQP_SERVER", "localhost"),
            int(os.environ.get("AMQP_PORT", 5672)),
            os.environ.get("QUEUE_NAME", "tiles")
        )

    host: str
    port: int
    queue_name: str