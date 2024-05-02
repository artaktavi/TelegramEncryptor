import telebot;
bot = telebot.TeleBot('7084095251:AAHigI_uMhc-CGP1L97MiVYgY2Jhlex4UIg');

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
    if message.text == "/help":
        bot.send_message(message.from_user.id, help_command_text)
    elif message.text == "/start":
        bot.send_message(message.from_user.id, start_command_text)
    elif message.text == "/cipher":
        # KEYBOARD
        bot.send_message()
    else:
        bot.send_message(message.from_user.id, wrong_command_text)

bot.polling(none_stop=True, interval=0)

