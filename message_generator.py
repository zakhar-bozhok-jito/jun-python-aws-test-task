from dataclasses import dataclass
import os
import pika
import json
from logging import basicConfig, getLogger, INFO
from tile_message import DownloadTileMessage
from amqp_common import retryingConnectionToAMQP, AMQPConfig

basicConfig(level=INFO)
logger = getLogger(__name__)

def generateTilesInSquare(x: int, y: int, zoom: int, x_size: int, y_size: int):
    for i in range(x, x + x_size):
        for j in range(y, y + y_size):
            yield DownloadTileMessage(i, j, zoom)

def getGoogleTileLinkAndSendToQueue(
    x: int, y: int, zoom: int, x_size: int, y_size: int, channel, queue_name: str
):
    for tile in generateTilesInSquare(x, y, zoom, x_size, y_size):
        jsonMessage = tile.toJSON()
        channel.basic_publish(
            exchange="", routing_key=queue_name, body=jsonMessage
        )

def getDeafultTileCoordinate():
    # x,y,zoom
    return (268396, 390159, 20)


def getDefaultDownloadGridSize():
    # x_size, y_size
    return (900, 900)

if __name__ == "__main__":
    amqpConfig = AMQPConfig.fromENV()
    tilesInfo = getDeafultTileCoordinate()
    connection, channel = retryingConnectionToAMQP(
        amqpConfig.host, amqpConfig.port, amqpConfig.queue_name
    )
    x, y, zoom = getDeafultTileCoordinate()
    x_size, y_size = getDefaultDownloadGridSize()
    getGoogleTileLinkAndSendToQueue(
        x, y, zoom, x_size, y_size, channel, amqpConfig.queue_name
    )
    logger.info(f'Done sending messages to queue: "{amqpConfig.queue_name}", sent {x_size * y_size} messages')
