"""
Central logger utility for Aditya Music Bot.

Provides a `send_log()` helper that broadcasts formatted event messages to
BOTH the configured logger channel AND the bot owner's DM. Any failure in
either send (permission errors, chat not found, bot not admin, user blocked
the bot, etc.) is silently absorbed so the bot never crashes because of
notification issues.

Also exposes `play_logs()` (backward-compatible with the previous behaviour)
that now hooks into the new central dispatcher.
"""

from typing import Optional

from pyrogram.enums import ParseMode

from Melody.utils.database import is_on_off, get_log_topic
from config import LOG_GROUP_ID, OWNER_ID


async def send_log(text: str, *, force: bool = False) -> None:
    """
    Broadcast a log message to:
      1. The configured logger channel (LOG_GROUP_ID).
      2. The bot owner's private DM (OWNER_ID).

    Any exceptions raised while sending to either destination are swallowed;
    the caller never has to worry about the notification pipeline crashing
    the bot. If ``force`` is False, the play-log toggle stored in the DB
    (``is_on_off(2)``) is respected.
    """
    from Melody import app  # local import to avoid circular deps

    # Respect the play-log toggle unless the caller forces a send
    if not force:
        try:
            if not await is_on_off(2):
                return
        except Exception:
            # If the DB check itself fails, still attempt to notify.
            pass

    # --- 1) Logger channel -----------------------------------------------
    if LOG_GROUP_ID:
        try:
            thread_id = None
            try:
                thread_id = await get_log_topic(LOG_GROUP_ID)
            except Exception:
                thread_id = None
            await app.send_message(
                chat_id=LOG_GROUP_ID,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                message_thread_id=thread_id if thread_id else None,
            )
        except Exception:
            # Channel send failed (bot not admin / channel not found / etc.)
            # → silently skip.
            pass

    # --- 2) Owner DM ------------------------------------------------------
    if OWNER_ID and OWNER_ID != LOG_GROUP_ID:
        try:
            await app.send_message(
                chat_id=OWNER_ID,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception:
            pass


def _fmt_user(user) -> str:
    """Return a compact HTML block describing a Telegram user."""
    if user is None:
        return "<i>Unknown user</i>"
    name = getattr(user, "mention", None) or getattr(user, "first_name", "User")
    username = getattr(user, "username", None)
    uid = getattr(user, "id", "N/A")
    lines = [
        f"<b>ɴᴀᴍᴇ :</b> {name}",
        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{username}" if username else "<b>ᴜsᴇʀɴᴀᴍᴇ :</b> <i>none</i>",
        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{uid}</code>",
    ]
    return "\n".join(lines)


def _fmt_chat(chat) -> str:
    """Return a compact HTML block describing a Telegram chat."""
    if chat is None:
        return "<i>Unknown chat</i>"
    title = getattr(chat, "title", None) or getattr(chat, "first_name", "Private")
    username = getattr(chat, "username", None)
    cid = getattr(chat, "id", "N/A")
    lines = [
        f"<b>ɢʀᴏᴜᴘ ɴᴀᴍᴇ :</b> {title}",
        f"<b>ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ :</b> @{username}" if username else "<b>ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ :</b> <i>none</i>",
        f"<b>ɢʀᴏᴜᴘ ɪᴅ :</b> <code>{cid}</code>",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# High-level helpers – used by handlers throughout the code base
# ---------------------------------------------------------------------------

async def log_start(user) -> None:
    """User pressed /start in a private chat."""
    text = (
        "<b>🚀 ᴀᴅɪᴛʏᴀ ᴍᴜsɪᴄ — ɴᴇᴡ ᴜsᴇʀ /sᴛᴀʀᴛ</b>\n\n"
        f"{_fmt_user(user)}"
    )
    await send_log(text, force=True)


async def log_group_added(chat, added_by=None) -> None:
    """Bot was added to a new group / supergroup."""
    text_parts = [
        "<b>➕ ᴀᴅɪᴛʏᴀ ᴀᴅᴅᴇᴅ ᴛᴏ ᴀ ɴᴇᴡ ᴄʜᴀᴛ</b>\n",
        _fmt_chat(chat),
    ]
    if added_by is not None:
        text_parts.append("\n<b>ᴀᴅᴅᴇᴅ ʙʏ :</b>")
        text_parts.append(_fmt_user(added_by))
    await send_log("\n".join(text_parts), force=True)


async def log_bot_blocked(user) -> None:
    """A user blocked the bot in DM."""
    text = (
        "<b>🚫 ʙᴏᴛ ʙʟᴏᴄᴋᴇᴅ</b>\n"
        "<i>ᴀ ᴜsᴇʀ ᴊᴜsᴛ ʙʟᴏᴄᴋᴇᴅ ᴀᴅɪᴛʏᴀ.</i>\n\n"
        f"{_fmt_user(user)}"
    )
    await send_log(text, force=True)


async def log_song_play(message, streamtype: str) -> None:
    """
    A song was requested (used by the /play, /vplay callback flow).
    Sends chat + user + query + stream-type details to the logger channel
    and the owner DM.
    """
    try:
        query_text = ""
        if getattr(message, "text", None):
            parts = message.text.split(None, 1)
            if len(parts) > 1:
                query_text = parts[1]
    except Exception:
        query_text = ""

    text = (
        "<b>🎵 ᴀᴅɪᴛʏᴀ ᴘʟᴀʏ ʟᴏɢ</b>\n\n"
        f"{_fmt_chat(message.chat)}\n\n"
        f"{_fmt_user(message.from_user)}\n\n"
        f"<b>ǫᴜᴇʀʏ :</b> {query_text or '<i>n/a</i>'}\n"
        f"<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}"
    )
    # Skip sending if the event originated inside the log channel itself
    try:
        if message.chat.id == LOG_GROUP_ID:
            return
    except Exception:
        pass
    await send_log(text)


# ---------------------------------------------------------------------------
# Backwards-compat wrapper – existing plugins still call play_logs()
# ---------------------------------------------------------------------------
async def play_logs(message, streamtype: Optional[str] = None) -> None:
    """Backward-compatible wrapper around :func:`log_song_play`."""
    await log_song_play(message, streamtype or "unknown")
    
