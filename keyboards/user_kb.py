from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_MENU


def create_inline_kb(width: int,
                     pref: str,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=pref + button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=pref + button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_kb_menu(mines):
    btn_mines: KeyboardButton = KeyboardButton(text=mines)
    btn_miners: KeyboardButton = KeyboardButton(text=LEXICON_MENU['miners'])
    btn_warehouse: KeyboardButton = KeyboardButton(text=LEXICON_MENU['warehouse'])
    btn_market: KeyboardButton = KeyboardButton(text=LEXICON_MENU['market'])
    btn_profile: KeyboardButton = KeyboardButton(text=LEXICON_MENU['profile'])
    btn_shop: KeyboardButton = KeyboardButton(text=LEXICON_MENU['shop'])
    menu_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_mines, btn_miners],
                                                                            [btn_warehouse, btn_market], [btn_profile, btn_shop]],
                                                                    resize_keyboard=True)
    return menu_user