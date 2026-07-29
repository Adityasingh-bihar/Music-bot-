from pyrogram.types import InlineKeyboardButton as Ikb, InlineKeyboardMarkup

from .functions import get_urls_from_text as is_url

class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, row_width: int = 3):
        self.inline_keyboard = []
        self.row_width = row_width
        super().__init__(inline_keyboard=self.inline_keyboard)

    def add(self, *args):
        for i in range(0, len(args), self.row_width):
            self.inline_keyboard.append(list(args[i : i + self.row_width]))
        return self

    def row(self, *args):
        self.inline_keyboard.append(list(args))
        return self

def keyboard(buttons_list, row_width: int = 2):
    buttons = InlineKeyboard(row_width=row_width)
    data = []
    for i in buttons_list:
        kwargs = {"text": str(i[0])}
        value = str(i[1])
        if is_url(value):
            kwargs["url"] = value
        else:
            kwargs["callback_data"] = value

        if len(i) > 2:
            kwargs["style"] = i[2]
        if len(i) > 3:
            kwargs["icon_custom_emoji_id"] = i[3]

        data.append(Ikb(**kwargs))
    buttons.add(*data)
    return buttons

def ikb(data: dict, row_width: int = 2):
    return keyboard(data.items(), row_width=row_width)
