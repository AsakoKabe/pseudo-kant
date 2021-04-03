import os
from telebot import TeleBot
from utils import NeuralKant
from keyboards import create_keyboard, create_markup_max_length, create_markup_top_k, create_markup_top_p, \
    create_markup_setting, create_markup_temperature


token: str = os.environ.get('BOT_TOKEN')
bot: TeleBot = TeleBot(token)
model: NeuralKant = NeuralKant()

keyboard = create_keyboard()
markup_settings = create_markup_setting()
markup_top_p, top_p_value= create_markup_top_p()
markup_top_k, top_k_value = create_markup_top_k()
markup_temperature, temperature_value = create_markup_temperature()
markup_max_length, max_length_value = create_markup_max_length()


@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, 'Немного философии от псевдо-Канта.\n'
                                      'Напиши первые предложения для генерации текста\n'
                                      'Для получения справки - /help\n'
                                      'Настрока параметров генерации текста - /settings\n'
                                      'Включить генерацию текста - /activate\n'
                                      'Отлючить генерацию текста - /deactivate',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.send_message(message.chat.id, 'Бот написан для проекта по философии.\n'
                                      'Дообучалась нейронная сеть ruGPT3small от сбербанка.\n'
                                      'Репозиторий - https://github.com/sberbank-ai/ru-gpts\n'
                                      'Почитать про то, как работает нейроная сеть - https://habr.com/ru/post/490842/\n'
                                      '\n'
                                      'Для обучения нейронной сети использовались произведения И. Канта:\n'
                                      'Основы метафизики нравственности\n'
                                      'Критика практического разума\n'
                                      'Критика чистого разума\n'
                                      'Критика способности суждения\n'
                                      '\n'
                                      'Так же доступна настройка параметров генерации текста(возможно еще не сделана)\n'
                                      'Почитать подробнее про параметры для генерации текста - '
                                      'https://huggingface.co/blog/how-to-generate\n',
                     )


@bot.message_handler(commands=['activate'])
def send_activate_bot(message):
    model.set_mode(True)
    bot.send_message(message.chat.id, 'Псевдо-Кант включен')


@bot.message_handler(commands=['deactivate'])
def send_deactivate_bot(message):
    model.set_mode(False)
    bot.send_message(message.chat.id, 'Псевдо-Кант выключен')


@bot.message_handler(commands=['settings'])
def send_setting_message(message):
    bot.send_message(message.chat.id, 'Меню для настройки параметров генерации текста\n', reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('param_'))
def callback_param(call):
    if call.data == 'param_top_k':
        bot.edit_message_text('Изменение числа наиболее вероятных следующих слов', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_top_k)
    elif call.data == 'param_top_p':
        bot.edit_message_text('Изменение совокупной вероятности для следующих слов', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_top_p)
    elif call.data == 'param_temperature':
        bot.edit_message_text('Изменение вероятности появления слов с большой вероятностью', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_temperature)
    elif call.data == 'param_max_length':
        bot.edit_message_text('Изменение максимальной длины текста', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_max_length)
    elif call.data == 'param_info':
        bot.send_message(call.message.chat.id, model)
    elif call.data == 'param_default':
        model.set_default()
        bot.send_message(call.message.chat.id, 'Параметры по умолчанию установлены')


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_top_k'))
def callback_change_top_k(call):
    for k in top_k_value:
        if call.data == f'change_top_k_{k}':
            model.set_top_k(k)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_top_p'))
def callback_change_top_p(call):
    for p in top_p_value:
        if call.data == f'change_top_p_{p}':
            model.set_top_p(p)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_temperature'))
def callback_change_temperature(call):
    for temp in temperature_value:
        if call.data == f'change_temperature_{temp}':
            model.set_temperature(temp)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_max_length_'))
def callback_change_max_length(call):
    for length in max_length_value:
        if call.data == f'change_max_length_{length}':
            model.set_max_length(length)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup_settings)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if model.get_mode():
        bot.send_chat_action(message.chat.id, action='typing')
        result_generation = model.generate_text(message.text)
        bot.send_message(message.chat.id, result_generation)


if __name__ == '__main__':
    bot.polling()
