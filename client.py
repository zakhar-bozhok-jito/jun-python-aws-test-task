from enum import auto
import os
from time import sleep
import pika
import json
from logging import basicConfig, getLogger, INFO
from tile_message import DownloadTileMessage
from amqp_common import retryingConnectionToAMQP, AMQPConfig
import requests

basicConfig(level=INFO)
logger = getLogger(__name__)

def getMessageFromQueue(channel, queue_name: str) -> None or str:
    method_frame, header_frame, body = channel.basic_get(queue_name, auto_ack=True)
    if body is None:
        return None
    return body.decode("utf-8")

def getTileMessageFromQueue(channel, queue_name: str) -> None or DownloadTileMessage:
    message = getMessageFromQueue(channel, queue_name)
    if message is None:
        return None
    return DownloadTileMessage.fromJSON(message)

def getAllTileMessagesFromQueue(channel, queue_name: str, onMessageReceived):
    while True:
        message = getTileMessageFromQueue(channel, queue_name)
        if message is None:
            break
        onMessageReceived(message)

def getGoogleTileLink(x: int, y: int, zoom: int) -> str:
    return f"http://mt0.google.com/vt?lyrs=s&x={x}&y={y}&z={zoom}"

def createFolderIfNotExists(folder_name: str) -> None:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def downloadTile(tile: DownloadTileMessage, folder: str) -> None:
    x, y, zoom = tile.x, tile.y, tile.zoom
    tile_link = getGoogleTileLink(x, y, zoom)
    tile_name = f"{x}_{y}_{zoom}.png"
    tile_path = os.path.join(folder, tile_name)
    response = requests.get(tile_link)
    if response.status_code != 200:
        logger.error(f"Failed to download tile: {tile_link}, status code: {response.status_code}")
        return
    with open(tile_path, "wb") as f:
        f.write(response.content)

def proceedMessagesAtInterval(channel, queue_name: str, onMessageReceived, interval_seconds: int):
    while True:
        getAllTileMessagesFromQueue(channel, queue_name, onMessageReceived)
        sleep(interval_seconds)

if __name__ == "__main__":
    amqpConfig = AMQPConfig.fromENV()
    tilesFolder = os.environ.get("TILES_FOLDER", "tiles")
    connection, channel = retryingConnectionToAMQP(
        amqpConfig.host, amqpConfig.port, amqpConfig.queue_name
    )

    tile_downloader = lambda tile: downloadTile(tile, tilesFolder)
    createFolderIfNotExists(tilesFolder)
    proceedMessagesAtInterval(channel, amqpConfig.queue_name, tile_downloader, 5)
