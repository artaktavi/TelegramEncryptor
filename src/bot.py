import telebot;
from telebot import types
from fcrypto import CommandHelper
import os

bot = telebot.TeleBot('7084095251:AAHigI_uMhc-CGP1L97MiVYgY2Jhlex4UIg');

wrong_hack_text = "No possibility for hacking vernam cipher"
wrong_hack_answer_text = "Извини, друг, такой шифр я взламывать не умею"
success_hack_answer_text = "Шифр взломан! Вот предполагаемый ключ: "

generate_answer_text = "Сгенерированный ключ: "

cipher = "caesar"
command_helper = CommandHelper()
temp_dir_name = "temp_in_out"
input_file_name = temp_dir_name + '/' + "temp_input_"
output_file_name = temp_dir_name + '/' + "result.txt"

mode = ""
is_document_flag = False
waiting_input = "input"
waiting_key = "key"
waiting_for = ""

hack_answer_text = "Принято. Пытаюсь взломать..."
input_answer_text = "Принято. Жду ключа для шифра..."
key_answer_text = "Код получил. Обрабатываю запрос..."

if not os.path.isdir(temp_dir_name):
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
Я тебя не понимаю, напиши /help, чтобы посмотреть доступные команды
"""

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])
def get_document_messages(message):
    global is_document_flag
    print("get_doc")
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, "wb") as finp:
        finp.write(downloaded_file)
    with open(file_name, "r") as finp:
        message.text = finp.read()
    get_text_messages(message)
    is_document_flag = True

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print("------- got_message -------")
    print("waiting: " + waiting_for)
    if waiting_for == "":
        proccess_command(message)
    elif waiting_for == waiting_input:
        catch_input(message)
    elif waiting_for == waiting_key:
        catch_key(message)
        

def catch_input(message):
    global waiting_for
    global is_document_flag 
    print("catch_input")
    with open(input_file_name, "w") as file_inp:
        file_inp.write(message.text)
    if mode == "-h":
        bot.send_message(message.from_user.id, hack_answer_text)
        hacked_key = command_helper.execute_hack(cipher, input_file_name)
        if hacked_key != wrong_hack_text:
            text_to_send = success_hack_answer_text + hacked_key
        else:
            text_to_send = wrong_hack_answer_text
        bot.send_message(message.from_user.id, text_to_send)
        waiting_for = ""
        is_document_flag = False
    else:
        bot.send_message(message.from_user.id, input_answer_text)
        waiting_for = waiting_key

def catch_key(message):
    global waiting_for
    global is_document_flag 
    key = message.text
    args = [mode, cipher, input_file_name, output_file_name, key] 
    print("catch_key: args:", *args)
    command_helper.process_request(args)
    doc = open(output_file_name, "rb")
    if is_document_flag:
        bot.send_document(message.from_user.id, doc)
    else:
        bot.send_message(message.from_user.id, doc.read())
    is_document_flag = False
    waiting_for = ""

def proccess_command(message):
    global waiting_for
    global mode
    print("proccess_command")
    if message.text == "/help":
        bot.send_message(message.from_user.id, help_command_text)
    elif message.text == "/start":
        bot.send_message(message.from_user.id, start_command_text)
    elif message.text == "/cipher":
        get_cipher(message);
    elif message.text == "/encrypt":
        bot.send_message(message.from_user.id, "Зашифровка в режиме: " + cipher)
        waiting_for = waiting_input
        print("encrypt: " + waiting_for)
        mode = "-e"
    elif message.text == "/decrypt":
        bot.send_message(message.from_user.id, "Расшифровка в режиме: " + cipher)
        waiting_for = waiting_input
        mode = "-d"
    elif message.text == "/generate":
        bot.send_message(message.from_user.id, "Генерация шифра в режиме: " + cipher)
        bot.send_message(message.from_user.id, generate_answer_text + command_helper.execute_generate(cipher))
        mode = "-g"
    elif message.text == "/hack":
        bot.send_message(message.from_user.id, "Взлом шифра в режиме: " + cipher)
        waiting_for = waiting_input
        mode = "-h"
    else:
        bot.send_message(message.from_user.id, wrong_command_text)
        waiting_for = ""


def get_cipher(message):
    print("get_cipher")
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
    global cipher
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
