from telebot import *
from telebot import types
import time
import random
import options
import gpt
import secret
import requests
import sys

bot = TeleBot(secret.api)

debug = secret.debug
svet = secret.svet
I = secret.I


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.text == "/start@IvanSkyBot" and message.chat.type != 'private':
        bot.reply_to(message, f"Приветствую тебя, {message.from_user.first_name}. Я многофункциональный бот. Чтобы узнать что я могу, напишите /help")

    elif message.chat.type == 'private':
        bot.reply_to(message, f"Привет, {message.from_user.first_name}. Чтобы задать вопрос, просто напиши мне его в чат, и я отвечу")


private = ("Вот список моих команд:\n\n"
        "/start - Запуск бота\n"
        "/help - Получение помощи\n"
        "/genqr - Генерация qr кода по текту\n"
        "/link - Сокращение ссылок\n"
        "/weather - Показывает погоду в указанном населённом пункте\n"
        "/currency - Курс обычных и криптовалют\n"
        "/cat - Отправляет случайную картинку с котиком\n"
        "/random - Генератор случайных чисел\n"
        "/speech - Перевод из текста в речь\n"
        "/wish - Пожелания/баги в работе бота"
        "/donate - Поддержка автора\n\n")

chat = ("*Мои возможности в чате:*\n\n"
        "*Данные обращения к боту нужно просто написать в чате, тогда бот вам ответит*\n"
        "Чтобы обратиться к нейросети напишите: *@IvanSkyBot <текст>*, и бот вам ответит\n\n"
        "*Баскет* - бросить мяч в корзину\n"
        "*Ролл* - подбросить кость\n"
        "*Казино* - сыграть в казино\n"
        "*Бойкиссер* - бот отправит вам случайный стикер с бойкиссером\n"
        "*Бот кто <текст>* - бот случайным образом выберет участника групыы и подберёт для него тот текст, который вы напишите\n"
        "*Бот шар <текст>* - бот ответит вам на ваш вопрос случайным образом\n"
        "*Бот скажи <текст>* - бот напишет тескт от вашего имени")


@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.type != 'private' and message.text.lower() == '/help@ivanskybot':
        # bot.reply_to(message, "Вот список моих команд:\n"
        # "/start - Запуск бота\n"
        # "/help - Получение помощи\n"
        # "/genqr - Генерация qr кода по текту \n(Использование: /genqr <текст>)\n"
        # "/link - Сокращение ссылок \n(Использование: /link <ссылка>)\n"
        # "/weather - Показывает погоду в указанном населённом пункте\n(Использование: /weather <населённый пункт>)\n"
        # "/currency - Показывает текущий курс валюты. По умолчанию выводит курс Доллара и Евро. Если вы ходите получить курс определённой валюты:\n/currency <аббревиатура валюты(USD, EUR...)>\n"
        # "/donate - Поддержка автора\n\n"

        # "Мои возможности в чате:\n"
        # "*Данные обращения к боту нужно просто написать в чате, тогда бот вам ответит*\n"
        # "Чтобы обратиться к нейросети напишите: *@IvanSkyBot <текст>*, и бот вам ответит\n"
        # "*Баскет* - бросить мяч в корзину\n"
        # "*Ролл* - подбросить кость\n"
        # "*Казино* - сыграть в казино\n"
        # "*Бойкиссер* - бот отправит вам случайный стикер с бойкиссером\n"
        # "*Бот кто <текст>* - бот случайным образом выберет участника групыы и подберёт для него тот текст, который вы напишите\n"
        # "*Бот шар <текст>* - бот ответит вам на ваш вопрос случайным образом\n"
        # "*Бот скажи <текст>* - бот напишет тескт от вашего имени", parse_mode='Markdown')
        bot.reply_to(message, f"{private}{chat}", parse_mode='Markdown')

    elif message.chat.type == 'private':
        # bot.reply_to(message, "Вот список моих команд:\n"
        # "/start - Запуск бота\n"
        # "/help - Получение помощи\n"
        # "/genqr - Генерация qr кода по текту \n(Использование: /genqr <текст>)\n"
        # "/link - Сокращение ссылок \n(Использование: /link <ссылка>)\n"
        # "/weather - Показывает погоду в данный момент, в указанном населённом пункте\n(Использование: /weather <населённый пункт>)\n"
        # "/currency - Показывает текущий курс валюты. По умолчанию выводит курс Доллара и Евро.\nЕсли вы ходите получить курс определённой валюты: /currency <аббревиатура валюты(USD, EUR...)>"
        # "/donate - Поддержка автора\n", parse_mode='Markdown')
        bot.reply_to(message, private, parse_mode='Markdown')


@bot.message_handler(commands=['/'])
def a(message):
    course = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    asd = sorted(list(course['Valute'].keys()))
    sr = ""
    for i in asd:
        sr += f"{i}, "
    bot.send_message(message.chat.id, f"Список доступных валют:\n{sr.rstrip(', ')}")


@bot.message_handler(commands=['cat'])
def cat(message):
    options.cat(message)


@bot.message_handler(commands=['id'])
def id(message):
    username = message.from_user.username
    premium = message.from_user.is_premium

    if username == None:
        username = "У вас нет username"
    else:
        username = f"@{message.from_user.username}"

    if premium == None:
        premium = "У вас нет премиума. Чтобы его купить, перейдите в бот: @PremiumBot"
    else:
        premium = "У вас есть премиум" 
    
    bot.send_message(message.chat.id, f"Твоё имя: {message.from_user.first_name}\nТвой Username: {username}\nТвой id: {message.from_user.id}\nНаличие премиума: {premium}")


@bot.message_handler(commands=['qrgen', 'genqr'])
def qr(message):
    options.generate_qr(message)


@bot.message_handler(commands=['random'])
def print_rand(message):
    options.rand(message)


@bot.message_handler(commands=['speech'])
def send_text_to_speech(message):
    options.get_speech(message)


@bot.message_handler(commands=['weather', 'погода'])
def weather(message):
    options.weather(message)


@bot.message_handler(commands=['currency'])
def print_currency(message):
    options.currency(message)


@bot.message_handler(commands=['link'])
def link_shot(message):
    options.link(message)


@bot.message_handler(commands=['wish'])
def wish(message):
    try:
        text = message.text[5:]
        bot.send_message(message.chat.id, "Пожелание отправлено!")
        options.send_debug(debug, 9436, f"Пожелание:{text}")
    except Exception:
        bot.send_message(message.chat.id, "Использование: /wish пожелание")


@bot.message_handler(commands=['donate'])
def donate(message):
    bot.reply_to(message, f"Поддержать автора:\nclck.ru/3GQWxZ", disable_web_page_preview=True)


@bot.message_handler(commands=['addsticker'])
def sticker(message):
    if message.from_user.id == I:
        try:
            text = message.text.split(' ')
            with open("/root/TGBOT/stickers.txt", "a") as file:
                file.write(f"\n{text[1]}")
                bot.send_message(message.chat.id, "Стикер успешно добавлен)")
        except Exception:
            bot.send_message(message.chat.id, "Не ввёл стикер, мдаааа")
    else:
        bot.send_message(message.chat.id, "Недорос ещё")


@bot.message_handler(commands=["tokens"])
def tokens(message):
    gpt.print_tokens(message)


@bot.message_handler(content_types=["audio", "document", "animation", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "poll"])
def another(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Я работаю только с текстом. Чтобы задать вопрос, просто напишите мне")



@bot.message_handler(content_types=['text'])
def response(message):

    echo = message.text.split(" ")
    answer = ""
    text = message.text.lower()
    try:
        # если сообщения поступают не в диалоге с ботом
        if message.chat.type != 'private':
            if message.from_user.is_bot and message.from_user.id != bot.get_me().id:
                print(message.text)

            if text == "бот" or text == "bot":
                bot.reply_to(message, "Работает!")

            if text == "ролл":
                bot.send_dice(message.chat.id, "🎲", message_thread_id=message.message_thread_id)

            if text == "казино" or text == "рулетка":
                bot.send_dice(message.chat.id, "🎰", message_thread_id=message.message_thread_id)

            if text == "баскет" or text == "баскетболл":
                bot.send_dice(message.chat.id, "🏀", message_thread_id=message.message_thread_id)

            if text == "футболл" or text == "болл":
                bot.send_dice(message.chat.id, "⚽️", message_thread_id=message.message_thread_id)

            if text == "мишень" or text == "дротик":
                bot.send_dice(message.chat.id, "🎯", message_thread_id=message.message_thread_id)

            if text == "боулинг":
                bot.send_dice(message.chat.id, "🎳", message_thread_id=message.message_thread_id)



            if text == "бойкиссер":
                with open("/root/TGBOT/stickers.txt", "r") as file: 
                    allText = file.read()
                    words = list(map(str, allText.split())) 
                    content = random.choice(words)
                bot.send_sticker(message.chat.id, content, message_thread_id=message.message_thread_id)


            if text.startswith("бот кто"):
                for i in range(2, len(echo)):
                    answer += echo[i] + " "

                admins = bot.get_chat_administrators(message.chat.id)
                list_users = []

                for user in admins:
                    list_users.append(f"[{user.user.first_name}](tg://openmessage?user_id={user.user.id})")

                response = random.choices(list_users, k=1)[0]
                if len(echo) > 2:
                    bot.send_message(message.chat.id, f"🔮Шар считает, что {response}, *{answer}*", parse_mode="Markdown", message_thread_id=message.message_thread_id)

                else:
                    bot.reply_to(message, "Вы не ввели запрос. Использование:\nБот кто <текст>")


            if text.startswith("бот скажи"):
                for i in range(2, len(echo)):
                    answer += echo[i] + " "

                if len(echo) > 2:
                    bot.send_message(message.chat.id, f"{answer[:-1]}\\. От: [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})", parse_mode="MarkdownV2", message_thread_id=message.message_thread_id)

                else:
                    bot.reply_to(message, f"Вы не ввели текст. Использование:\nБот скажи <текст> ")


            if text.startswith("бот шар"):
                words = ["Да", "Частично", "Хз", "Нет", "Не совсем", "100%"]
                if len(echo) > 2:
                    response = random.choices(words, weights=[18, 19, 20, 17, 21, 14], k=1)[0]
                    bot.reply_to(message, f"🔮 [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id}), Я думаю: *{response}*", parse_mode='MarkdownV2')

                else:
                    bot.reply_to(message, "Вы не ввели текст. Использование:\n Бот шар <Текст>")


            # CHATGPT в группе
            if text.startswith("@ivanskybot"):
                for i in range(1, len(echo)):
                    answer += echo[i] + " "

                if answer:
                    gpt.start_gpt(message, answer.capitalize())

                else:
                    bot.send_message(message.chat.id, "Вы ввели пустой запрос.\nЧтобы спросить у ChatGpt:\n@IvanSkyBot <сообщение>")

            # END

            if message.reply_to_message is not None and message.reply_to_message.from_user.id == bot.get_me().id:
                gpt.start_gpt(message, text)


            if text.startswith("/dick"):
                   chanse = random.random()
                   lol = ["Пиписку меряешь?", "Вот это дааа", "Большая пиписка", "Куда больше..", "КХМ.."]
                   result = random.choice(lol)
                   if chanse <= 0.4:
                       bot.reply_to(message, result)


        # CHATGPT в диалоге с ботом
        else:
            if message.text.startswith('/'):
                bot.send_message(message.chat.id, "Такой комманды не существует. Для справки введите /help")
            else:
                gpt.start_gpt(message, message.text)

            # END

    except Exception as e:
        options.send_debug(debug, 2977, f"MAIN ERROR:\n{e}")



if __name__ == "__main__":
    gpt.update_get_token()
    options.start_time(svet)
    gpt.potok()
    bot.infinity_polling(timeout=60)
