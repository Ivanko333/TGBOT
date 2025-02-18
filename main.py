from telebot import *
import options
import gpt
import secret
import sqlite3

bot = TeleBot(secret.api)


@bot.message_handler(commands=['server'])
def send_ping(message):
    a = options.ping(secret.server)
    bot.reply_to(message, a)


@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(message.chat.id, "Поддержать автора: clck.ru/3GQWxZ")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Привет, {message.from_user.first_name}")


@bot.message_handler(commands=['off'])
def off(message):
    bot.send_message(message.chat.id, "Размечтался...")


@bot.message_handler(content_types=['text'])
def response(message):

    debug = -1002495044873
    chat_bot = 7093269631
    echo = message.text.split(" ")
    answer = ""

    if message.chat.id != chat_bot:
        if message.text.lower() == "test":
            bot.send_message(message.chat.id, 'Привет!')

        if message.text.lower() == "бот":
            bot.reply_to(message, "Работает!")

        if message.text.lower() == "lol":
            bot.send_message(message.chat.id, 'Ага')

        if message.text.lower() == "iann dior" or message.text.lower() == "iann door":
            bot.reply_to(message, "Этот тот который nigga? 0_0")

        if message.text.lower() == "топ":
            bot.reply_to(message, "Ты топ!")

        if message.text == "Ирис":
            bot.reply_to(message, "Жмот!")

        if message.text.lower() == "кис кис" or message.text.lower() == "кис-кис":
            bot.reply_to(message, "Мяу!")

        if message.text.lower() == "кис кис кис":
            bot.reply_to(message, "ЖЕНЩИНА СЮРПРИЗ")

        if message.text == "Броен":
            bot.reply_to(message, "Я украла Брайна")

        if message.text == "Работает":
            bot.reply_to(message, "Конечно работаю))")

        if message.text == "Привет":
            bot.send_message(message.chat.id, "Ку ку")

        if message.text == "Хы" or message.text == "Хых":
            bot.send_message(message.chat.id, '😁')

        if message.text.lower() == "telebot":
            bot.reply_to(message, "Да, это именна та библиоzтека, на которой я сделан 😁")

        if message.text == ".api":
            bot.reply_to(message, message)

        if message.text == "Бу":
            bot.send_message(message.chat.id, "Бу! Испугался? Не бойся, я друг, я тебя не обижу. Иди сюда, иди ко мне, "
                                              "сядь рядом со мной, посмотри мне в глаза."
                                              "Ты видишь меня? Я тоже тебя вижу. Давай смотреть друг на друга до тех пор, "
                                              "пока наши глаза не устанут. Ты не хочешь?"
                                              "Почему? Что-то не так?")

        if echo[0].lower() == "спросить":
            for i in range(1, len(echo)):
                answer += echo[i] + " "

            bot.send_message(message.chat.id, gpt.ask_gpt(answer))

    else:
        bot.send_message(message.chat.id, gpt.ask_gpt(message.text))


bot.infinity_polling()
