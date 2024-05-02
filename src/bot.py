import telebot;
from telebot import types
from fcrypto import CommandHelper
import os

bot = telebot.TeleBot('7084095251:AAHigI_uMhc-CGP1L97MiVYgY2Jhlex4UIg');

cipher = "caesar"
command_helper = CommandHelper()
is_waiting_for = ""
temp_dir_name = "./temp_in_out"

os.makedirs(temp_dir_name)

help_command_text = """
Привет, с тобой на связи TCrypto бот!

Я могу помочь тебе с шифровкой / дешифровкой текстовых сообщений и файлов. Во мне заложена поддержка шифров:

- Цезаря
- Виженера
- Вернама

А также я умею генерировать случайный ключ для одного из этих шифров и взламывать тексты, зашифрованные методом Цезаря при помощи частотного анализа.

Чтобы начать работу со мной или просто познакомиться с вариантами использования, напиши /start
"""


start_command_text = """
Привет, с тобой на связи TCrypto бот!

Я создан и предназначен для шифровки / дешифровки текстовых сообщений и файлов, это, собственно, весь мой функционал.

Вот список моих команд:

- Используй /help, чтобы получить основную информацию

- Напиши /cipher, чтобы поменять используемый шифр, по умолчанию это шифр Цезаря

- Чтобы зашифровать сообщение или файл, используй команду /encrypt, после отправь сообщение (файл), а следующим сообщением - код, который будет использоваться для зашифровки

- Чтобы расшифровать сообщение или файл, используй /decrypt, после отправь сообщение (файл), а следующим сообщением - код, который будет использоваться для дешифровки

"""

wrong_command_text = """
Я тебя не понимаю, напиши /start, чтобы посмотреть доступные команды
"""

@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    if is_waiting_for:
        print("yey")
    else:
        if message.text == "/help":
            bot.send_message(message.from_user.id, help_command_text)
        elif message.text == "/start":
            bot.send_message(message.from_user.id, start_command_text)
        elif message.text == "/cipher":
            get_cipher(message);
        elif message.text == "/encrypt":
            bot.send_message(message.from_user.id, "Твой шифр: " + cipher)
            command_helper.execute_encypher(cipher, "debug/input.txt", "debug/output.txt", 5)
        else:
            bot.send_message(message.from_user.id, wrong_command_text)

def get_cipher(message):
    keyboard = types.InlineKeyboardMarkup()
    key_caesar = types.InlineKeyboardButton(text='Цезарь', callback_data='caesar')
    keyboard.add(key_caesar)
    key_vernam = types.InlineKeyboardButton(text='Вернам', callback_data='vernam')
    keyboard.add(key_vernam)
    key_vigener = types.InlineKeyboardButton(text='Виженер', callback_data='vigener')
    keyboard.add(key_vigener)
    question = "Выбери шифр, который хочешь использовать:"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "caesar":
        cipher = call.data
        bot.send_message(call.message.chat.id, 'Запомню, шифр Цезаря');
    elif call.data == "vernam":
        cipher = call.data
        bot.send_message(call.message.chat.id, 'Запомню, шифр Вернама');
    elif call.data == "vigener":
        cipher = call.data
        bot.send_message(call.message.chat.id, 'Запомню, шифр Виженера');
    else:
        bot.send_message(call.message.chat.id, 'Ошибка! Некорректный запрос');

bot.polling(none_stop=True, interval=0)

os.rmdir(temp_dir_name)
