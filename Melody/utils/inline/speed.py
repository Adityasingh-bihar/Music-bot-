from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def speed_markup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="0.5x", callback_data=f"SpeedUP {chat_id}|0.5", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994408240673197462"),
                InlineKeyboardButton(text=_["P_B_4"], callback_data=f"SpeedUP {chat_id}|1.0", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994583930605407777"),
                InlineKeyboardButton(text="2.0x", callback_data=f"SpeedUP {chat_id}|2.0", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5992263196566621814"),
            ],
            [
                InlineKeyboardButton(text="0.75x", callback_data=f"SpeedUP {chat_id}|0.75", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994803897355472919"),
                InlineKeyboardButton(text="1.5x", callback_data=f"SpeedUP {chat_id}|1.5", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994535689532739650"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5992179264315723303"),
            ],
        ]
    )
    return upl
