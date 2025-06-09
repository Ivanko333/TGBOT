from telebot import *
import datetime
import time
import threading
import os
import random
import requests
from requests.exceptions import RequestException, Timeout
from urllib.parse import urlparse
import secret
import base64
from speechify import Speechify
import keyboard
from io import BytesIO
from pydub import AudioSegment


bot = TeleBot(secret.api)
debug = secret.debug
I = secret.I


def send_debug(chat_id, topic_id, message_text):
    bot.send_message(chat_id=chat_id, message_thread_id=topic_id, text=message_text)


def check_time(chat_id):
    while True:
        now = datetime.datetime.now()
        if (now.weekday() == 0 and now.time().hour == 17 and now.time().minute == 0) or (now.weekday() == 2 and now.time().hour == 17 and now.time().minute == 0):
            bot.send_message(chat_id, "❗❗❗Тренировка, @smartkondra❗❗❗")
        time.sleep(30)


def start_time(chat_id):
    thread = threading.Thread(target=check_time, args=(chat_id,))
    thread.daemon = True
    thread.start()


def link(message):
    try:
        text = message.text.split(' ')
        response = requests.get(f'https://clck.ru/--?url={text[1]}')
        bot.send_message(message.chat.id, response.content, disable_web_page_preview=True, message_thread_id=message.message_thread_id)
    
    except Exception:
        bot.reply_to(message, "Использование команды: /link ссылка")


def generate_qr(message):
    text = message.text.split(' ')
    result = ""
    if len(text) > 1:
        for i in range(1, len(text)):
            result += text[i] + " "

        response = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?data={result}&size=500x500")
        bot.send_photo(message.chat.id, response.content, message_thread_id=message.message_thread_id)
    else:
        bot.reply_to(message, "Использование команды:\n/genqr текст")


def weather(message):
    text = message.text.split(" ")
    result = ""
    for i in range(1, len(text)):
        result += text[i] + "+"

    try:
        if len(text) > 1:
            wheather_now = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={result[:-1]}&lang=ru&appid={secret.weather}&units=metric").json()
            url = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={result[:-1]}&appid={secret.weather}&lang=ru&units=metric").json()['list']
            res = "🗓Прогноз на день:\n"
            for i in range(10):
                date = datetime.datetime.strptime(url[i]['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                res += f"• {date}: {round(url[i]['main']['temp'], 1)}°C - {url[i]['weather'][0]['description']}. Ветер: {round(url[i]['wind']['speed'], 1)} м/с\n"

            city = wheather_now['name']
            #get_time = requests.get(f"https://timezone.abstractapi.com/v1/current_time/?api_key=aa8e48c45f33446097626af6d156d0ad&location={city}").json()
            #a = get_time['datetime'].split(" ")
            #date = a[0][8:]
            #mounth = a[0][5:][:-3]
            #year = a[0][:4]
            #hour = a[1][:-3]
            #time = f"{hour}, {date}.{mounth}.{year}"
            bot.send_message(message.chat.id, f"🏙Погода в городе - {wheather_now['name']}:\n\n"
          f"⌛️Сейчас:\n• {round(wheather_now['main']['temp'], 1)}°C - {wheather_now['weather'][0]['description']}\n"
          f"• Ощущается как: {round(wheather_now['main']['feels_like'], 1)}°C\n"
          f"• Ветер: {round(wheather_now['wind']['speed'], 1)} м/с\n"
          #f"• Время: {time}\n\n"
          f"{res}", message_thread_id=message.message_thread_id)
        
        else:
            bot.reply_to(message, "❓Введите город. Например: /weather Москва")

    except KeyError:
        bot.reply_to(message, "🤔 Хмм.. Не знаю такого города")


def rand(message):
    text = message.text.split(' ')
    if len(text) == 2:
        num = random.randint(1, int(text[1]))
        bot.send_message(message.chat.id, f"Число: {num}", message_thread_id=message.message_thread_id)        
    
    elif len(text) == 3:
        num = random.randint(int(text[1]), int(text[2]))
        bot.send_message(message.chat.id, f"Число: {num}", message_thread_id=message.message_thread_id)
    
    else:
        bot.reply_to(message, "Использование команды:\n/random число (от 1 до заданного числа)\n/random число1 число2 (от число1 до число2)")


def cat(message):
    text = message.text.split(" ")
    if len(text) == 1:
        cat = requests.get("https://cataas.com/cat").content
        bot.send_photo(message.chat.id, cat, message_thread_id=message.message_thread_id)
    else:
        result = ""
        for i in range(1, len(text)):
            result += text[i] + "%20"
        cat = requests.get(f"https://cataas.com/cat/says/{result}").content
        bot.send_photo(message.chat.id, cat, message_thread_id=message.message_thread_id)        


def crypto(message, key, nominal=1):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': secret.crypto
    }
    parameters_usd = {
        'symbol': key,
        'convert': 'USD'
    }
    parameters_rub = {
        'symbol': key,
        'convert': 'RUB'
    }

    try:
        response_usd = requests.get(url, params=parameters_usd, headers=headers).json()
        response_rub = requests.get(url, params=parameters_rub, headers=headers).json()
        price_usd = round(response_usd['data'][key]['quote']['USD']['price']* nominal, 3)
        price_rub = round(response_rub['data'][key]['quote']['RUB']['price']* nominal, 3)
        return f"💸Цена {key}: {price_usd}$ / {price_rub}₽"

    except KeyError:
        bot.reply_to(message, f"❌ Такой валюты нет")
        return None

    except Exception as e:
        bot.reply_to(message, "🔁 Попробуйте ещё раз")
        send_debug(debug, 2977, f"CURRENCY ERROR:\n{e}")
        return None


def currency(message):
    text = message.text.upper().split(" ")
    course = requests.request("GET", "https://www.cbr-xml-daily.ru/daily_json.js").json()
    if len(text) == 1:
        bot.send_message(message.chat.id, f"💰{course['Valute']['USD']['Name']}: {round(course['Valute']['USD']['Value'], 2)}₽\n"
        f"💰{course['Valute']['EUR']['Name']}: {round(course['Valute']['EUR']['Value'], 2)}₽\n"
        f"{crypto(message, "BTC")}\n"
        f"{crypto(message, "XMR")}\n\n"
        f"Если вы хотите узнать курс других валют:\n/currency валюта(Например: /currency CNY)", message_thread_id=message.message_thread_id)

    else:
        try:
            nominal = course['Valute'][text[1]]['Nominal']
            name = course['Valute'][text[1]]['Name']
            value = course['Valute'][text[1]]['Value']
            value = round(value / nominal, 2)
            bot.send_message(message.chat.id, f"💰Курс {name}: {value}₽", message_thread_id=message.message_thread_id)

        except KeyError:
            try:
                func = crypto(message, text[1], float(text[2].replace(',', '.')))
            except IndexError:
                func = crypto(message, text[1])
            except ValueError:
                bot.reply_to(message, "Введите число")
            if func:
                bot.send_message(message.chat.id, func, message_thread_id=message.message_thread_id)



def get_speech(message):
    text = message.text.split(" ")
    try:
        if len(text) != 1 and len(text) < 1500:
            feedback = ""
            for i in range(1, len(text)):
                feedback += text[i] + " "

            client = Speechify(token=secret.speech_api)        
            voice = client.tts.audio.speech(
                audio_format="ogg",
                input= " " + feedback,
                language="ru-RU",
                model="simba-multilingual",
                voice_id="arkady"
            )

            data = voice.audio_data
            speech = base64.b64decode(data)
            bot.send_voice(message.chat.id, speech, message_thread_id=message.message_thread_id)
        else:
            bot.reply_to(message, "Введите текст который вы хотите озвучить(Не более 1500 символов).\nНапример: /speech Привет")

    except Exception as e:
        bot.reply_to(message, "⚠️Произошла ошибка")
        send_debug(debug, 2977, f"SPEECH ERROR:\n{e}")

