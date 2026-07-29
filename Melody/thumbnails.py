from __future__ import annotations

import asyncio
import io
import os
from pathlib import Path
from typing import Optional

import aiohttp
from PIL import Image, ImageDraw, ImageFont
from py_yt import VideosSearch

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Canvas & Palette
# ---------------------------------------------------------------------------
W, H = 1280, 720

C_BG        = "#FFFFFF"
C_BLACK     = "#111111"
C_MID       = "#666666"
C_MUTED     = "#AAAAAA"
C_LIGHT     = "#EBEBEB"
C_ACCENT    = "#111111"
C_GREEN     = "#1DB954"

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
def _get_font(size: int):
    f_path = "Melody/assets/font2.ttf"
    if not os.path.exists(f_path):
        f_path = "Melody/assets/font.ttf"
    try:
        return ImageFont.truetype(f_path, size=size)
    except Exception:
        try:
            return ImageFont.load_default(size=size)
        except Exception:
            return ImageFont.load_default()

_F_WATERMARK  = _get_font(380)
_F_LABEL      = _get_font(24)
_F_TITLE      = _get_font(85)
_F_ARTIST     = _get_font(45)
_F_STAT       = _get_font(24)
_F_TIME       = _get_font(22)
_F_BRAND      = _get_font(24)

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
PAD_X        = 90
PAD_Y        = 90
ART_SIZE     = 460
ART_X        = W - PAD_X - ART_SIZE
ART_Y        = (H - ART_SIZE) // 2

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _truncate(text: Optional[str], font, max_px: int, draw: ImageDraw.ImageDraw) -> str:
    text = str(text or "")
    if draw.textlength(text, font=font) <= max_px:
        return text
    while text and draw.textlength(text + "…", font=font) > max_px:
        text = text[:-1]
    return text + "…" if text else ""

def _wrap_text(text: Optional[str], font, max_width: int, draw: ImageDraw.ImageDraw, max_lines: int = 2) -> list[str]:
    text = str(text or "")
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if draw.textlength(" ".join(current_line), font=font) > max_width:
            current_line.pop()
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            if len(lines) == max_lines - 1:
                break
    
    # Handle the last line
    if current_line:
        remaining_text = " ".join(words[words.index(current_line[0]):])
        lines.append(_truncate(remaining_text, font, max_width, draw))
    return lines

def _safe_text(draw, xy, text, font, fill):
    text = str(text or "")
    try:
        draw.text(xy, text, font=font, fill=fill)
    except Exception:
        draw.text(xy, text, font=_get_font(22), fill=fill)

# Icons
def _icon_play(draw, cx, cy, r=28, bg=C_BLACK, fg="#FFFFFF"):
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=bg)
    h = r // 2 + 2
    draw.polygon([(cx - h//2 + 3, cy - h), (cx - h//2 + 3, cy + h), (cx + h + 1, cy)], fill=fg)

def _icon_skip(draw, cx, cy, size=18, c=C_MID, fwd=True):
    h = size // 2
    if fwd:
        draw.polygon([(cx - h, cy - h), (cx - h, cy + h), (cx + 2, cy)], fill=c)
        draw.rectangle([(cx + 3, cy - h), (cx + 7, cy + h)], fill=c)
    else:
        draw.polygon([(cx + h, cy - h), (cx + h, cy + h), (cx - 2, cy)], fill=c)
        draw.rectangle([(cx - 7, cy - h), (cx - 3, cy + h)], fill=c)

def _icon_shuffle(draw, cx, cy, size=18, c=C_MUTED):
    s = size
    x, y = cx - s // 2, cy - s // 2
    draw.line([(x, y + s//3), (x + s, y)], fill=c, width=2)
    draw.line([(x, y + s*2//3), (x + s, y + s)], fill=c, width=2)

def _icon_repeat(draw, cx, cy, size=18, c=C_MUTED):
    r = size // 2
    draw.arc([(cx - r, cy - r), (cx + r, cy + r)], 40, 320, fill=c, width=2)
    draw.polygon([(cx + r - 5, cy - 5), (cx + r + 3, cy - 1), (cx + r - 3, cy + 5)], fill=c)

# ---------------------------------------------------------------------------
# Fetch & Render
# ---------------------------------------------------------------------------
async def _fetch_all(videoid: str, session: aiohttp.ClientSession):
    title = "Unknown Title"
    channel = "Unknown Channel"
    t_url = None
    
    # 1. 100% accurate extraction via YouTube oEmbed
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={videoid}&format=json"
    try:
        async with session.get(oembed_url) as resp:
            if resp.status == 200:
                data = await resp.json()
                title = data.get("title") or title
                channel = data.get("author_name") or channel
                t_url = data.get("thumbnail_url") or t_url
    except Exception as e:
        print(f"[gen_thumb_typo] oembed error: {e}")

    # 2. Supplementary metadata via VideosSearch
    dur = "0:00"
    views = "—"
    year = "—"
    try:
        results = VideosSearch(videoid, limit=1)
        meta = (await results.next())["result"][0]
        dur = meta.get("duration") or "0:00"
        views = meta.get("viewCount", {}).get("short") or "—"
        year = (meta.get("publishedTime") or "")[:4] or "—"
        
        # If oEmbed failed, fallback to VideosSearch
        if title == "Unknown Title":
            title = meta.get("title") or "Unknown Title"
            channel = meta.get("channel", {}).get("name") or "Unknown"
            thumbs = meta.get("thumbnails", [])
            if not t_url and thumbs:
                t_url = thumbs[0]["url"].split("?")[0]
    except Exception as e:
        print(f"[gen_thumb_typo] meta error: {e}")

    raw = None
    if t_url:
        try:
            async with session.get(t_url) as r:
                if r.status == 200:
                    data = await r.read()
                    raw_full = Image.open(io.BytesIO(data)).convert("RGB")
                    w, h = raw_full.size
                    m = min(w, h)
                    raw = raw_full.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
        except Exception as e:
            pass

    return title, dur, views, channel, year, raw

def _render(title: str, duration: str, views: str, channel: str, year: str, album_img: Optional[Image.Image], track_num: int, username: str, progress_ratio: float) -> Image.Image:
    img = Image.new("RGB", (W, H), C_BG)
    draw = ImageDraw.Draw(img)

    # Accent bar
    draw.rectangle([(0, 0), (W, 8)], fill=C_ACCENT)

    # Huge subtle watermark centered behind the left text
    wmark = str(track_num or 1).zfill(2)
    _safe_text(draw, (PAD_X - 10, PAD_Y - 50), wmark, _F_WATERMARK, "#F7F7F7")

    # Left Column setup
    max_text_w = W - (PAD_X * 2) - ART_SIZE - 40
    
    # Section Label
    _safe_text(draw, (PAD_X, PAD_Y), "N O W   P L A Y I N G", _F_LABEL, C_MUTED)

    # Title wrapping
    lines = _wrap_text(title, _F_TITLE, max_text_w, draw, max_lines=2)
    ty = PAD_Y + 50
    for line in lines:
        _safe_text(draw, (PAD_X, ty), line, _F_TITLE, C_BLACK)
        ty += 95
    
    # Artist
    artist_y = ty + 10
    _safe_text(draw, (PAD_X, artist_y), _truncate(channel, _F_ARTIST, max_text_w, draw), _F_ARTIST, C_MID)

    # Controls Row (Anchored to the bottom left)
    ctrl_y = H - PAD_Y - 60
    cx = PAD_X
    _icon_shuffle(draw, cx + 15, ctrl_y, size=22, c=C_MUTED); cx += 65
    _icon_skip(draw, cx + 15, ctrl_y, size=20, c=C_MID, fwd=False); cx += 55
    _icon_play(draw, cx + 28, ctrl_y, r=28); cx += 85
    _icon_skip(draw, cx + 15, ctrl_y, size=20, c=C_MID, fwd=True); cx += 55
    _icon_repeat(draw, cx + 15, ctrl_y, size=22, c=C_MUTED)

    # Progress bar (Above Controls)
    bar_y = ctrl_y - 50
    try:
        p_ratio = float(progress_ratio or 0)
    except (ValueError, TypeError):
        p_ratio = 0.0
    fill_px = int(max_text_w * max(0.0, min(1.0, p_ratio)))
    draw.line([(PAD_X, bar_y), (PAD_X + max_text_w, bar_y)], fill=C_LIGHT, width=4)
    if fill_px:
        draw.line([(PAD_X, bar_y), (PAD_X + fill_px, bar_y)], fill=C_BLACK, width=4)
    dot_x = PAD_X + fill_px
    draw.ellipse([(dot_x - 8, bar_y - 8), (dot_x + 8, bar_y + 8)], fill=C_BLACK)

    # Timestamps
    duration = str(duration or "0:00")
    _safe_text(draw, (PAD_X, bar_y + 15), "0:00", _F_TIME, C_MUTED)
    dur_w = draw.textlength(duration, font=_F_TIME)
    _safe_text(draw, (PAD_X + max_text_w - dur_w, bar_y + 15), duration, _F_TIME, C_MUTED)

    # Right Column: Huge Album Art
    if album_img:
        art = album_img.resize((ART_SIZE, ART_SIZE), Image.Resampling.LANCZOS)
        img.paste(art, (ART_X, ART_Y))
    else:
        draw.rectangle([(ART_X, ART_Y), (ART_X + ART_SIZE, ART_Y + ART_SIZE)], fill=C_LIGHT)
    
    draw.rectangle([(ART_X, ART_Y), (ART_X + ART_SIZE, ART_Y + ART_SIZE)], outline=C_LIGHT, width=2)

    # Stats overlay beneath album art
    stat_str = f"{views} plays  •  {year}"
    stat_w = draw.textlength(stat_str, font=_F_STAT)
    _safe_text(draw, (ART_X + (ART_SIZE - stat_w)//2, ART_Y + ART_SIZE + 25), stat_str, _F_STAT, C_MID)

    # Branding (Bottom right)
    brand = f"Powered by @{username or 'MelodyBot'}"
    brand_w = draw.textlength(brand, font=_F_BRAND)
    _safe_text(draw, (W - PAD_X - brand_w + 20, H - PAD_Y + 10), brand, _F_BRAND, C_GREEN)

    return img

async def gen_thumb(videoid: str, username: Optional[str] = None, track_num: int = 1, progress_ratio: float = 0.3) -> str:
    output_path = CACHE_DIR / f"typo_{videoid}.jpg"
    if output_path.exists():
        return str(output_path)

    try:
        if username is None:
            try:
                from Melody import app
                username = app.username
            except Exception:
                username = "MelodyBot"

        async with aiohttp.ClientSession() as session:
            title, duration, views, channel, year, raw = await _fetch_all(videoid, session)

        img = _render(title, duration, views, channel, year, raw, track_num, username, progress_ratio)
        img.save(output_path, "JPEG", quality=92, optimize=True, subsampling=0)
        return str(output_path)
    except Exception as e:
        print(f"[gen_thumb] Failed to generate thumbnail for {videoid}: {e}")
        from config import YOUTUBE_IMG_URL, _DEFAULT_IMG
        return YOUTUBE_IMG_URL or _DEFAULT_IMG