from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
import config
from Melody import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5258108352008823107"
            ),
            InlineKeyboardButton(
                text=_["S_B_2"], url=f"https://t.me/{config.SUPPORT_GROUP}",
                icon_custom_emoji_id="5258215846450305872"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴀʙᴏᴜᴛ", callback_data="about_page",
                icon_custom_emoji_id="5258093637450866522"
            ),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id="5258108352008823107"
            )
        ],
        [
            InlineKeyboardButton(
                text="ᴀʙᴏᴜᴛ", callback_data="about_page",
                icon_custom_emoji_id="5258093637450866522"
            ),
            InlineKeyboardButton(
                text="ᴏᴡɴᴇʀ", callback_data="owner_page",
                icon_custom_emoji_id="5258011929993026890"
            ),
        ],
          [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_page_1",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id="5258328383183396223"
            ),
        ],
    ]
    return buttons

def about_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{config.SUPPORT_CHANNEL}",
                icon_custom_emoji_id="5260268501515377807"
            ),
            InlineKeyboardButton(
                text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{config.SUPPORT_GROUP}",
                icon_custom_emoji_id="5258215846450305872"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"], callback_data="settingsback_helper",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            )
        ]
    ]
    return buttons

def owner_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_12"], user_id=config.OWNER_ID,
                icon_custom_emoji_id="5258011929993026890"
            ),
            InlineKeyboardButton(
                text=_["S_B_5"], user_id=config.DEV_ID,
                icon_custom_emoji_id="5258011929993026890"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"], callback_data="settingsback_helper",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5260342697075416641"
            ),
        ]
    ]
    return buttons
