from telebot import *
import requests
import json
import secret
import time
from datetime import datetime
import options

bot = TeleBot(secret.api)
time1 = None
debug = secret.debug

def update_time():
    global time1
    while True:
        time1 = datetime.now()
        time.sleep(30)


def potok():
    update_thread = threading.Thread(target=update_time)
    update_thread.daemon = True
    update_thread.start()


def back(message, response):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {secret.token_gpt}", "Content-Type": "application/json"},

            data=json.dumps({
                "model": "google/gemini-2.0-pro-exp-02-05:free",
                "messages": [
                    {"role": "system", "content": [ {"type": "text", "text": f"Ты умный бот, помогающий пользователям и отвечающий только по русски(RU). Твой создатель Ivanko333. Сегодня/Дата: {time1}"} ] },
                    {"role": "user", "content": [ {"type": "text", "text": response} ] }
                ],
                "max_tokens": 1000,
                "temperature": 0.6,
                "top_p": 0.3
            })
        )
        shit = json.loads(json.loads(json.dumps(response.text)))
        message_content = shit['choices'][0]['message']['content']
        bot.send_message(message.chat.id, message_content)

    except KeyError:
        back(message, response)

    except Exception as e:
        options.send_debug(debug, 2977, e)
        bot.send_message(message.chat.id, "Пожалуйста, попробуйте ещё раз")
    time.sleep(5)


def start_gpt(message, response):
    thread = threading.Thread(target=back, args=(message, response,))
    thread.daemon = True
    thread.start()


def link(message, user_url):
    endpoint = 'https://clck.ru/--'
    url = (user_url, '?utm_source=sender')
    response = requests.get(endpoint, params={'url': url})
    bot.reply_to(message, response.text, disable_web_page_preview=True)


def generate_qr(message, text_qr):
    response = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?data={text_qr}&size=500x500")
    bot.send_photo(message.chat.id, response.content)
    
    
