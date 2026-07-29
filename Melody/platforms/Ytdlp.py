import asyncio
import os
from typing import Union
from os import path
import yt_dlp

from Melody.utils.formatters import seconds_to_min
from Melody import LOGGER
import config


class YtDlpAPI:
    """
    Generic media platform handler using yt-dlp.
    Acts as a catch-all for URLs not handled by YouTube, Spotify, etc.
    Supports ~1000+ sites (Facebook, Instagram, Twitter/X, Twitch, etc.)
    """

    def __init__(self):
        self.opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "format": "best",
            "retries": 5,
            "nooverwrites": False,
            "no_warnings": True,
            "quiet": True,
            "no_cache_dir": True,
            "nocheckcertificate": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "http_headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
            },
            "cookiefile": "cookies.txt" if path.exists("cookies.txt") else None,
        }

    async def valid(self, link: str) -> bool:
        """
        Checks if the URL is supported by yt-dlp using the modern API.
        """
        def _check_valid():
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                try:
                    info = ydl.extract_info(link, download=False, process=False)
                    return info is not None
                except yt_dlp.utils.DownloadError:
                    return False
                except Exception:
                    return False

        try:
            return await asyncio.get_event_loop().run_in_executor(None, _check_valid)
        except Exception as e:
            LOGGER(__name__).error(f"Error in YtDlp.valid: {e}")
        return False

    async def track(self, link: str) -> tuple:
        """
        Extracts track metadata without downloading.
        """
        def _extract():
            with yt_dlp.YoutubeDL(self.opts) as ydl:
                return ydl.extract_info(link, download=False)

        try:
            info = await asyncio.get_event_loop().run_in_executor(None, _extract)
            if not info:
                return {"title": "Unknown", "duration_min": None, "thumb": config.YOUTUBE_IMG_URL}, None

            duration = info.get("duration", 0)
            duration_min = seconds_to_min(duration) if duration else None
            thumbnail = info.get("thumbnail") or info.get("thumbnails", [{}])[0].get("url") or config.YOUTUBE_IMG_URL

            track_details = {
                "title": info.get("title", "Unknown Title"),
                "link": link,
                "vidid": info.get("id", "ytdlp"),
                "duration_min": duration_min,
                "duration_sec": duration,
                "thumb": thumbnail.split("?")[0] if thumbnail != config.YOUTUBE_IMG_URL else thumbnail,
            }
            return track_details, info.get("id", "ytdlp")
        except Exception as e:
            LOGGER(__name__).error(f"Error in YtDlp.track: {e}")
            return {"title": "Unknown", "duration_min": None, "thumb": config.YOUTUBE_IMG_URL}, None

    async def download(self, url: str) -> tuple:
        """
        Downloads media from the given URL via yt-dlp.
        Returns (track_details_dict, file_path_str) on success, or (False, False) on failure.
        """
        def _download():
            with yt_dlp.YoutubeDL(self.opts) as ydl:
                return ydl.extract_info(url, download=True)

        try:
            info = await asyncio.get_event_loop().run_in_executor(None, _download)
            if not info:
                return False, False

            ext = info.get("ext", "mp4")
            file_path = path.join("downloads", f"{info.get('id', 'ytdlp')}.{ext}")

            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                duration = info.get("duration", 0)
                duration_min = seconds_to_min(duration) if duration else None
                thumbnail = info.get("thumbnail", config.YOUTUBE_IMG_URL)
                track_details = {
                    "title": info.get("title", "Unknown Title"),
                    "link": url,
                    "vidid": info.get("id", "ytdlp"),
                    "duration_sec": duration,
                    "duration_min": duration_min,
                    "uploader": info.get("uploader", "Unknown"),
                    "filepath": file_path,
                    "thumb": thumbnail,
                }
                return track_details, file_path
            return False, False
        except Exception as e:
            LOGGER(__name__).error(f"Error in YtDlp.download: {e}")
            return False, False
