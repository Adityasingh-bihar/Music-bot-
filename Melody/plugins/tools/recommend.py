from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Melody import app, YouTube
from Melody.utils.decorators.language import language
from Melody.misc import db
from config import BANNED_USERS

@app.on_message(filters.command(["suggest"]) & ~BANNED_USERS)
@language
async def suggest_command(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["sugg_1"])

    query = message.text.split(None, 1)[1]
    mystic = await message.reply_text(_["play_1"])

    try:
        suggestions = await YouTube.get_suggestions(query)
        if not suggestions or not suggestions.get("result"):
            return await mystic.edit_text(_["sugg_3"])

        text = _["sugg_2"].format(query)
        for i, suggestion in enumerate(suggestions["result"][:10], 1):
            text += f"{i}➻ <code>{suggestion}</code>\n"

        await mystic.edit_text(text)
    except Exception:
        await mystic.edit_text(_["play_3"])

@app.on_message(filters.command(["recommend", "related"]) & filters.group & ~BANNED_USERS)
@language
async def recommend_command(client, message: Message, _):
    chat_id = message.chat.id
    if chat_id not in db or not db[chat_id]:
        return await message.reply_text(_["general_5"])

    current_track = db[chat_id][0]
    video_id = current_track.get("vidid")

    if not video_id or video_id in ["telegram", "soundcloud", "ytdlp"] or video_id.startswith("http"):
         return await message.reply_text(_["play_14"])

    mystic = await message.reply_text(_["play_1"])

    try:
        related = await YouTube.get_related(video_id)
        if not related or not related.get("result"):
            return await mystic.edit_text(_["sugg_3"])

        text = _["sugg_4"]
        buttons = []
        for i, track in enumerate(related["result"][:5], 1):
            title = track["title"][:35]
            duration = track["duration"]
            vidid = track["id"]
            text += f"{i}➻ <b>{title}</b> ({duration})\n"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"Play {i}",
                        callback_data=f"MusicStream {vidid}|{message.from_user.id}|a|g|d"
                    )
                ]
            )

        buttons.append([InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")])
        await mystic.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception:
        await mystic.edit_text(_["play_3"])
