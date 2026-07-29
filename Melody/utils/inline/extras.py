from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

from config import SUPPORT_GROUP

def botplaylist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_9"], url=f"https://t.me/{SUPPORT_GROUP}", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5258215846450305872"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5260342697075416641"),
        ],
    ]
    return buttons

def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=ButtonStyle.DANGER,
                    icon_custom_emoji_id="5260342697075416641"
                ),
            ]
        ]
    )
    return upl

def supp_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_9"],
                    url=f"https://t.me/{SUPPORT_GROUP}",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id="5258215846450305872"
                ),
            ]
        ]
    )
    return upl
