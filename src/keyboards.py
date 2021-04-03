from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Tuple, List


def create_keyboard() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(True)
    keyboard.row('/start', '/help', '/settings')
    keyboard.row('/activate', '/deactivate')

    return keyboard


def create_markup_setting() -> InlineKeyboardMarkup:
    markup_settings: InlineKeyboardMarkup = InlineKeyboardMarkup()

    markup_settings.add(InlineKeyboardButton("Максимальная длина текста",
                                             callback_data='param_max_length'))
    markup_settings.add(InlineKeyboardButton("Число наиболее вероятных следующих слов",
                                             callback_data='param_top_k'))
    markup_settings.add(InlineKeyboardButton("Совокупная вероятность для следующих слов",
                                             callback_data='param_top_p'))
    markup_settings.add(InlineKeyboardButton("Вероятность появления слов с большой вероятностью",
                                             callback_data='param_temperature'))
    markup_settings.add(InlineKeyboardButton("Узнать текущее параметры",
                                             callback_data='param_info'))
    markup_settings.add(InlineKeyboardButton("Установить параметры по умолчанию",
                                             callback_data='param_default'))

    return markup_settings


def create_markup_max_length() -> Tuple[InlineKeyboardMarkup, List[int]]:
    markup_max_length: InlineKeyboardMarkup = InlineKeyboardMarkup()
    max_length_value: List[int] = [10, 50, 100, 200, 300, 500]
    for length in max_length_value:
        markup_max_length.add(
            InlineKeyboardButton(f'{length}', callback_data=f'change_max_length_{length}'))
    markup_max_length.add(InlineKeyboardButton('Назад', callback_data='change_back'))

    return markup_max_length, max_length_value


def create_markup_top_k() -> Tuple[InlineKeyboardMarkup, List[int]]:
    markup_top_k: InlineKeyboardMarkup = InlineKeyboardMarkup()
    top_k_value: List[int] = [1, 2, 3, 5, 10, 15, 20]
    for k in top_k_value:
        markup_top_k.add(InlineKeyboardButton(f'{k}', callback_data=f'change_top_k_{k}'))
    markup_top_k.add(InlineKeyboardButton("Назад", callback_data='change_back'))

    return markup_top_k, top_k_value


def create_markup_top_p() -> Tuple[InlineKeyboardMarkup, List[float]]:
    markup_top_p: InlineKeyboardMarkup = InlineKeyboardMarkup()
    top_p_value: List[float] = [0.1, 0.5, 0.2, 0.8, 0.9, 0.95, 1]
    for p in top_p_value:
        markup_top_p.add(InlineKeyboardButton(f'{p}', callback_data=f"change_top_p_{p}"))
    markup_top_p.add(InlineKeyboardButton("Назад", callback_data='change_back'))

    return markup_top_p, top_p_value


def create_markup_temperature() -> Tuple[InlineKeyboardMarkup, List[float]]:
    markup_temperature: InlineKeyboardMarkup = InlineKeyboardMarkup()
    temperature_value: List[float] = [0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 1]
    for temp in temperature_value:
        markup_temperature.add(
            InlineKeyboardButton(f'{temp}', callback_data=f"change_temperature_{temp}"))
    markup_temperature.add(InlineKeyboardButton("Назад", callback_data='change_back'))

    return markup_temperature, temperature_value
