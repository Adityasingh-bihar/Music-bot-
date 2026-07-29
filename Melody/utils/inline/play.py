import math
from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
from Melody.utils.formatters import time_to_seconds
from Melody import app
from Melody.misc import db

"""
Inline keyboard markups for music playback and stream control.
Provides various button layouts for searching, playing, and managing streams.
"""

def track_markup(_, videoid, user_id, channel, fplay):
    """Buttons for selecting audio or video when a single track is searched."""
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],  # Audio
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5258289810082111221"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],  # Video
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5258152182150077732"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            )
        ],
    ]
    return buttons


def suggestion_markup(_, videoid, user_id):
    """Markup for suggested/related tracks."""
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],  # Audio
                callback_data=f"MusicStream {videoid}|{user_id}|a|g|d",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5258289810082111221"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],  # Video
                callback_data=f"MusicStream {videoid}|{user_id}|v|g|d",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5258152182150077732"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            )
        ],
    ]
    return buttons

def stream_markup_timer(_, chat_id, played, dur, is_playing=True):
    """Buttons for an active stream with a progress bar and playback controls."""
    # Calculate progress bar
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec > 0 else 0
    umm = math.floor(percentage)
    filled = min(10, math.floor(umm / 10))
    bar = "▰" * filled + "▱" * (10 - filled)

    # Show queue button only if there are items in the queue
    queue_len = len(db.get(chat_id, []))
    q_btn = []
    if queue_len > 1:
        videoid = db.get(chat_id)[0]['vidid']
        q_btn = [InlineKeyboardButton(text="☰", callback_data=f"GetQueued g|{videoid}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5257969839313526622")]

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                url=f"https://t.me/{app.username}?startgroup=true",
                icon_custom_emoji_id="5359529383319084413"
            )
        ],
        [
            InlineKeyboardButton(text="❚❚" if is_playing else "▷", callback_data=f"ADMIN Toggle|{chat_id}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994291189929480156"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5260450573768990626"),
            InlineKeyboardButton(text="■", callback_data=f"ADMIN Stop|{chat_id}", style=ButtonStyle.DANGER, icon_custom_emoji_id="5994472239980875497"),
        ],
        q_btn,
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5260342697075416641"),
        ],
    ]
    # Filter out empty rows (like q_btn if queue is not long enough)
    return [row for row in buttons if row]


def stream_markup(_, chat_id, is_playing=True):
    """Buttons for an active stream without a timer bar (used for live streams or simple view)."""
    queue_len = len(db.get(chat_id, []))
    q_btn = []
    if queue_len > 1:
        videoid = db.get(chat_id)[0]['vidid']
        q_btn = [InlineKeyboardButton(text="☰", callback_data=f"GetQueued g|{videoid}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5257969839313526622")]

    buttons = [
        [
            InlineKeyboardButton(text="❚❚" if is_playing else "▷", callback_data=f"ADMIN Toggle|{chat_id}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994291189929480156"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5260450573768990626"),
            InlineKeyboardButton(text="■", callback_data=f"ADMIN Stop|{chat_id}", style=ButtonStyle.DANGER, icon_custom_emoji_id="5994472239980875497"),
        ],
        q_btn,
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5260342697075416641"),
        ],
    ]
    return [row for row in buttons if row]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    """Buttons for selecting audio or video when a playlist is searched."""
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MelodyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5257965174979042426"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MelodyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5257965174979042426"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            ),
        ],
    ]
    return buttons

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    """Buttons for confirming playback of a live stream."""
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],  # Live Stream
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id="5258152182150077732"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            ),
        ],
    ]
    return buttons

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    """Navigation buttons for search result sliders."""
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text="←",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id="5260687119092817530"
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            ),
            InlineKeyboardButton(
                text="→",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id="5258420634785947640"
            ),
        ],
    ]
    return buttons
