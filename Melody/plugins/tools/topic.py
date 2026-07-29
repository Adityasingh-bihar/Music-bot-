from pyrogram import filters
from pyrogram.types import Message
from Melody import app
from Melody.utils.database import set_topic, delete_topic, get_topic
from Melody.utils.permissions import adminsOnly
from Melody.utils.formatters import to_small_caps

@app.on_message(filters.command(["settopic"]) & filters.group)
@adminsOnly("can_change_info")
async def set_topic_command(client, message: Message):
    if not message.topic_message:
        return await message.reply_text("» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ғᴏʀᴜᴍ ᴛᴏᴘɪᴄs.")

    topic_id = message.message_thread_id
    await set_topic(message.chat.id, topic_id)
    await message.reply_text(
        f"✅ <b>{to_small_caps('Dedicated topic set.')}</b>\n"
        f"ᴀʟʟ ʙᴏᴛ ɪɴᴛᴇʀᴀᴄᴛɪᴏɴs ᴡɪʟʟ ɴᴏᴡ sᴛᴀʏ ɪɴ ᴛʜɪs ᴛᴏᴘɪᴄ.\n\n"
        f"<i>(Note: Commands used in other topics will still be responded to in this dedicated topic if playback is active)</i>"
    )

@app.on_message(filters.command(["deltopic"]) & filters.group)
@adminsOnly("can_change_info")
async def del_topic_command(client, message: Message):
    topic_id = await get_topic(message.chat.id)
    if not topic_id:
        return await message.reply_text("» ᴛʜᴇʀᴇ ɪs ɴᴏ ᴅᴇᴅɪᴄᴀᴛᴇᴅ ᴛᴏᴘɪᴄ sᴇᴛ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.")

    await delete_topic(message.chat.id)
    await message.reply_text(f"🗑️ <b>{to_small_caps('Dedicated topic removed.')}</b>")

@app.on_message(filters.command(["topic"]) & filters.group)
async def topic_status_command(client, message: Message):
    topic_id = await get_topic(message.chat.id)
    if not topic_id:
        await message.reply_text("» ɴᴏ ᴅᴇᴅɪᴄᴀᴛᴇᴅ ᴛᴏᴘɪᴄ sᴇᴛ. ʙᴏᴛ ᴡɪʟʟ ʀᴇᴘʟʏ ɪɴ ᴛʜᴇ sᴀᴍᴇ ᴛᴏᴘɪᴄ ᴡʜᴇʀᴇ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ᴜsᴇᴅ.")
    else:
        await message.reply_text(f"📌 <b>{to_small_caps('Dedicated topic ID')}:</b> <code>{topic_id}</code>")
