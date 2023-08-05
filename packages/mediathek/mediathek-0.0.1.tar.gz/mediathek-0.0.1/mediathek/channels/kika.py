import requests
from datetime import datetime

from .base import BaseChannel
from ..models import Video, VideoResolution, Brand


class Kika(BaseChannel):
    BASE_API_URL = "https://prod.kinderplayer.cdn.tvnext.tv/api"

    def all_videos(self):
        r = requests.get(f"{self.BASE_API_URL}/videos")
        videos = r.json()["_embedded"]["items"]
        results = []

        for video_data in videos:
            results.append(KikaVideo(video_data, channel=self))

        return results

    def video(self, id):
        r = requests.get(f"{self.BASE_API_URL}/videos/{id}")
        return KikaVideo(r.json(), channel=self)

    def all_brands(self):
        r = requests.get(f"{self.BASE_API_URL}/brands")
        brands = r.json()["_embedded"]["items"]
        results = []

        for brand_data in brands:
            results.append(KikaBrand(brand_data, channel=self))

        return results

    def brand(self, id):
        r = requests.get(f"{self.BASE_API_URL}/brands/{id}")
        return KikaBrand(r.json(), channel=self)

    @staticmethod
    def _parse_date(raw_date):
        return datetime.now()


class KikaVideo(Video):
    def __init__(self, data, channel):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.appear_date = Kika._parse_date(data["appearDate"])
        self.expiration_date = Kika._parse_date(data["expirationDate"])
        self.channel = self
        self.brand = KikaBrand(data["_embedded"]["brand"], channel=channel)

    def download_urls(self):
        r = requests.get(f"{Kika.BASE_API_URL}/videos/{self.id}/player-assets")
        results = []

        for resolution in r.json()["hbbtvAssets"]:
            results.append(
                VideoResolution(
                    url=resolution["url"],
                    resolution=resolution["quality"].split(" | ")[-1]
                )
            )

        return results


class KikaBrand(Brand):
    def __init__(self, data, channel):
        self.id = data["id"]
        self.title = data["title"]
        self.total_videos = data["totalVideos"]
        # Some brands do not have a description
        self.description = data.get("description")
        self.channel = channel

    def all_videos(self):
        r = requests.get(f"{Kika.BASE_API_URL}/brands/{self.id}/videos")
        videos = r.json()["_embedded"]["items"]
        results = []

        for video_data in videos:
            results.append(KikaVideo(video_data, channel=self))

        return results
