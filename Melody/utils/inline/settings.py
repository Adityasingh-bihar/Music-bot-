from typing import Union

from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle

def setting_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994444846679461852"),
            InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994376075663118156"),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994581796006662272"),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994680146462772772"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5992179264315723303"),
        ],
    ]
    return buttons

def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="Voting Mode", callback_data="VOTEANSWER", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994440311193997179"),
            InlineKeyboardButton(
                text=_["ST_B_5"] if mode == True else _["ST_B_6"],
                callback_data="VOMODECHANGE",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id="5994592593554444039"
            ),
        ],
        [
            InlineKeyboardButton(text="➖ 2", callback_data="FERRARIUDTI M", icon_custom_emoji_id="5992060014548750359"),
            InlineKeyboardButton(
                text=f"Current: {current}",
                callback_data="ANSWERVOMODE",
                icon_custom_emoji_id="5994472239980875497"
            ),
            InlineKeyboardButton(text="➕ 2", callback_data="FERRARIUDTI A", icon_custom_emoji_id="5994749106457678661"),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5447506720316225765"
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5992179264315723303"),
        ],
    ]
    return buttons

def auth_users_markup(_, status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_7"], callback_data="AUTHANSWER", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994411195610698057"),
            InlineKeyboardButton(
                text=_["ST_B_8"] if status == True else _["ST_B_9"],
                callback_data="AUTH",
                style=ButtonStyle.SUCCESS,
                icon_custom_emoji_id="5992249676009574065"
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AUTHLIST", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5994389450191278223"),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5447506720316225765"
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5992179264315723303"),
        ],
    ]
    return buttons

def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
    AudQuality: str = "HIGH",
    VidQuality: str = "HD_720p",
):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_10"], callback_data="SEARCHANSWER", icon_custom_emoji_id="5994416353866420697"),
            InlineKeyboardButton(
                text=_["ST_B_11"] if Direct else _["ST_B_12"],
                callback_data="MODECHANGE",
                icon_custom_emoji_id="5994759766566506299"
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_13"], callback_data="AUTHANSWER", icon_custom_emoji_id="5994483127722971224"),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Group else _["ST_B_9"],
                callback_data="CHANNELMODECHANGE",
                icon_custom_emoji_id="5994539481988861796"
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_14"], callback_data="PLAYTYPEANSWER", icon_custom_emoji_id="5994788920804511598"),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Playtype else _["ST_B_9"],
                callback_data="PLAYTYPECHANGE",
                icon_custom_emoji_id="5994392954884591478"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=ButtonStyle.DANGER,
                icon_custom_emoji_id="5447506720316225765"
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER, icon_custom_emoji_id="5992179264315723303"),
        ],
    ]
    return buttons
