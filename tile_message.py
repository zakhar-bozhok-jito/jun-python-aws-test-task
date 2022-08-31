from dataclasses import dataclass
import json

@dataclass
class DownloadTileMessage:
    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.zoom = zoom

    def toJSON(self) -> str:
        return json.dumps({
            "x": self.x,
            "y": self.y,
            "zoom": self.zoom
        })

    @staticmethod
    def fromJSON(json_str: str) -> "DownloadTileMessage":
        json_dict = json.loads(json_str)
        return DownloadTileMessage(
            json_dict["x"],
            json_dict["y"],
            json_dict["zoom"]
        )
