import telebot;
from telebot import types
from fcrypto import CommandHelper
import os

bot = telebot.TeleBot('7084095251:AAHigI_uMhc-CGP1L97MiVYgY2Jhlex4UIg');

wrong_hack_text = "No possibility for hacking vernam cipher"
wrong_hack_answer_text = "Извини, друг, такой шифр я взламывать не умею"
success_hack_answer_text = "Шифр взломан! Вот предполагаемый ключ: "

generate_answer_text = "Сгенерированный ключ: "

error_answer_text = "ой... что-то пошло не так, попробуй повторить запрос сначала"

cipher = "caesar"
command_helper = CommandHelper()
temp_dir_name = "temp"
input_file_name = temp_dir_name + '/' + "temp_input.txt"
output_file_name = temp_dir_name + '/' + "result.txt"

mode = ""
is_document_flag = False
waiting_input = "input"
waiting_key = "key"
waiting_for = ""

hack_answer_text = "Принято. Пытаюсь взломать..."
enter_input_answer_text = "Введи текстовое сообщение / отправь текстовый файл"
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

А также я умею генерировать случайный ключ для этих шифров и взламывать тексты, зашифрованные методом Цезаря при помощи частотного анализа.

Чтобы начать работу со мной или просто познакомиться с вариантами использования, напиши /start
"""

start_command_text = """
Привет, с тобой на связи TCrypto бот!

Я создан и предназначен для шифровки / дешифровки текстовых сообщений и файлов, это, собственно, весь мой функционал.

Текст может быть произвольным, однако к ключам есть некоторые требования:

- Цезарь: ключ должен быть натуральным числом в диапазоне от 3 до 50

- Виженер: ключ должен иметь длину не более 30 символов и может состоять только из символов:
ABCDEFGHIJKLMNOPQRSTUVWXY

- Вернам: ключ должен иметь длину не более 30 символов и может состоять только из символов:
123456789:;@<=>?ABCDEFGHIJKLMNOPQRSTUVWXY

Вот список моих команд:

- Используй команду /help, чтобы получить основную информацию

- Используй команду /cipher, чтобы поменять используемый шифр, по умолчанию это шифр Цезаря

- Используй команду /encrypt, чтобы зашифровать сообщение или файл, после отправь сообщение (файл), а следующим сообщением - ключ, который будет использоваться для зашифровки

- Используй команду /decrypt, чтобы расшифровать сообщение или файл, после отправь сообщение (файл), а следующим сообщением - ключ, который будет использоваться для дешифровки

- Используй команду /hack, чтобы попробовать взломать шифр, после отправь текст, который хочешь взломать. TCrypto умеет взламывать только шифр Цезаря

- Используй команду /generate, чтобы сгенерировать случайный ключ для текущего шифра
"""

wrong_command_text = """
Я тебя не понимаю, напиши /start, чтобы посмотреть доступные команды
"""

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])
def get_document_messages(message):
    global is_document_flag
    print("------- DOCUMENT -------")
    print("from: " + message.from_user.username)
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(input_file_name, "wb") as file_inp:
        file_inp.write(downloaded_file)
    is_document_flag = True
    process_message(message)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print("------- MESSAGE -------")
    print("from: " + message.from_user.username)
    print("waiting: " + waiting_for)
    process_message(message)

def process_message(message):
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
    if not is_document_flag:
        with open(input_file_name, "w") as file_inp:
            file_inp.write(message.text)
    if mode == "-h":
        bot.send_message(message.from_user.id, hack_answer_text)
        try:
            hacked_key = command_helper.execute_hack(cipher, input_file_name)
            bot.send_message(message.from_user.id, success_hack_answer_text + hacked_key)
        except:
            bot.send_message(message.from_user.id, error_answer_text)
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
    try:
        command_helper.process_request(args)
    except:
        bot.send_message(message.from_user.id, error_answer_text)
        is_document_flag = False
        waiting_for = ""
        return
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
        bot.send_message(message.from_user.id, "Зашифровка в режиме: " + cipher + '\n' + enter_input_answer_text)
        waiting_for = waiting_input
        print("encrypt: " + waiting_for)
        mode = "-e"
    elif message.text == "/decrypt":
        bot.send_message(message.from_user.id, "Расшифровка в режиме: " + cipher + '\n' + enter_input_answer_text)
        waiting_for = waiting_input
        mode = "-d"
    elif message.text == "/generate":
        bot.send_message(message.from_user.id, "Генерация шифра в режиме: " + cipher)
        bot.send_message(message.from_user.id, generate_answer_text + command_helper.execute_generate(cipher))
        mode = "-g"
    elif message.text == "/hack":
        bot.send_message(message.from_user.id, "Взлом шифра в режиме: " + cipher + '\n' + enter_input_answer_text)
        if (cipher != "caesar"):
            bot.send_message(message.from_user.id, wrong_hack_answer_text)
        else:
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
    print("------- KEYBOARD -------")
    print("from: " + call.from_user.username)
    print("data: " + call.data)
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

if os.path.exists(input_file_name):
    os.remove(input_file_name)

if os.path.exists(output_file_name):
    os.remove(output_file_name)

os.rmdir(temp_dir_name)
