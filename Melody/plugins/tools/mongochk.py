import re
import asyncio

from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from pyrogram import filters
from pyrogram.types import Message

from Melody import app

mongo_url_pattern = re.compile(r"mongodb(?:\+srv)?:\/\/[^\s]+")

@app.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ\n`Ex: /mongochk your_mongodb_url`"
        )

    # Extract URL safely, even if there are spaces within parameters
    mongo_url = message.text.split(None, 1)[1]
    
    # Immediately delete the message for privacy (it contains their database credentials!)
    try:
        await message.delete()
    except Exception:
        pass

    if re.match(mongo_url_pattern, mongo_url):
        # Send a temporary checking message
        msg = await message.reply("⏳ ᴄʜᴇᴄᴋɪɴɢ ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛɪᴏɴ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
        
        try:
            # Use AsyncMongoClient so we don't block the bot's event loop
            client_db = AsyncMongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            
            # Use asyncio.wait_for to enforce the timeout check
            await asyncio.wait_for(client_db.server_info(), timeout=6.0)
            
            await msg.edit("ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ɪs ᴠᴀʟɪᴅ ᴀɴᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ sᴜᴄᴇssғᴜʟ ✅")
        except asyncio.TimeoutError:
            await msg.edit("❌ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛɪᴍᴇᴅ ᴏᴜᴛ. Cʜᴇᴄᴋ ɪғ ʏᴏᴜʀ Iᴘ is ᴡʜɪᴛᴇʟɪsᴛᴇᴅ sᴇᴛ ᴛᴏ '0.0.0.0/0'!")
        except OperationFailure as e:
            # Authentication failed or bad privileges
            await msg.edit(f"❌ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ: {e.details.get('errmsg', str(e))}")
        except Exception as e:
            # Other errors like bad connection string
            error_msg = str(e)
            if len(error_msg) > 100:
                error_msg = error_msg[:100] + "..."
            await msg.edit(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴍᴏɴɢᴏᴅʙ: {error_msg}")
        finally:
            if 'client_db' in locals():
                client_db.close()
    else:
        await message.reply("ᴜᴘs! ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ғᴏʀᴍᴀᴛ ɪs ɪɴᴠᴀʟɪᴅ")

__MODULE__ = "Mᴏɴɢᴏᴅʙ"
__HELP__ = """
**ᴍᴏɴɢᴏᴅʙ ᴄʜᴇᴄᴋᴇʀ:**

• `/mongochk [mongo_url]`: Cʜᴇᴄᴋs ᴛʜᴇ ᴠᴀʟɪᴅɪᴛʏ ᴏғ ᴀ ᴍᴏɴɢᴏᴅʙ URL ᴀɴᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴏɴɢᴏᴅʙ ɪɴsᴛᴀɴᴄᴇ.
"""
