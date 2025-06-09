from telebot import *
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from datetime import datetime
import time
import requests
import json
import secret
import options
import threading
from requests.packages import urllib3
import uuid
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


bot = TeleBot(secret.api)
time_now = None
date = None
debug = secret.debug
giga_token = ""

payload = Chat(
    messages=[
    Messages(role=MessagesRole.SYSTEM, content=f"Отвечай только по русски(RU). Сегодня/Дата:{date}. Время:{time_now}. Твоё имя(ассистент) - IvaSky")
    ],

temperature=0.6,
max_tokens=2000 )


def get_token(scope='GIGACHAT_API_PERS'):
    global giga_token
    while True:
        rq_uid = str(uuid.uuid4())
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': rq_uid,
            'Authorization': f'Basic {secret.giga}'
        }
        payload = {
            'scope': scope
        }

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            giga_token = response.json()['access_token']

        except Exception as e:
            options.send_debug(debug, 2977, f"GET TOKEN ERROR\n{e}")
        time.sleep(600)


def print_tokens(message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/balance"
    payload = {}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Bearer {giga_token}'
    }

    response = requests.get(url, headers=headers, data=payload, verify=False)
    tokens = ""
    try:
        tokens = response.json()['balance']
        list = ""
        for i in range(len(tokens)):
            list += f"Модель: {tokens[i]['usage']} Токены: {tokens[i]['value']}\n"
        bot.send_message(message.chat.id, list)
    
    except Exception as e:
        options.send_debug(debug, 2977, f"PRINT_TOKENS ERROR:\n{response.json()}")


def back(message, response_user):
    with GigaChat(credentials=secret.giga, verify_ssl_certs=False, model="GigaChat") as giga:
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            payload.messages.append(Messages(role=MessagesRole.USER, content=response_user))
            response = giga.chat(payload)
            content = response.choices[0].message
            payload.messages.append(content)
            bot.reply_to(message, content.content)
            options.send_debug(debug, 2977, f"@{message.from_user.username}")
        
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка =( Попробуйте ещё раз", message_thread_id=message.message_thread_id)
            options.send_debug(debug, 2977, f"GPT ERROR:\n{e}")


def update_get_token():
    thread1 = threading.Thread(target=get_token)
    thread1.daemon = True
    thread1.start()


def update_time():
    global time_now, date
    while True:
        time_now = datetime.now().strftime("%H:%M")
        date = datetime.now().strftime("%B %d, %Y")
        time.sleep(30)


def potok():
    update_thread = threading.Thread(target=update_time)
    update_thread.daemon = True
    update_thread.start()


def start_gpt(message, response):
    thread = threading.Thread(target=back, args=(message, response,))
    thread.daemon = True
    thread.start()



# def back(message, response_user):
#     try:
#         msg1 = bot.send_message(message.chat.id, "Бот думает. Ожидайте ответ в течениии 5-10 секунд")
#         bot.send_chat_action(message.chat.id, 'typing')
#         response = requests.post(
#             url="https://openrouter.ai/api/v1/chat/completions",
#             headers={"Authorization": f"Bearer {secret.token_gpt}", "Content-Type": "application/json"},

#             data=json.dumps({
#                 "model": "google/gemini-2.0-flash-exp:free",
#                 "messages": [
#                     {"role": "system", "content": [ {"type": "text", "text": f"Ты умный бот, помогающий пользователям и отвечающий только по русски(RU). Сегодня/Дата: {time_now}"} ] },
#                     {"role": "user", "content": [ {"type": "text", "text": response_user} ] }
#                 ],
#                 "max_tokens": 1000,
#                 "temperature": 0.5,
#                 "top_p": 0.3
#             })
#         )
#         shit = json.loads(json.loads(json.dumps(response.text)))
#         print(shit)
#         message_content = shit['choices'][0]['message']['content']
#         bot.delete_message(message.chat.id, msg1.message_id)
#         bot.send_message(message.chat.id, message_content)
#         options.send_debug(debug, 2977, f"@{message.from_user.username}")
#     except Exception as e:
#         options.send_debug(debug, 2977, e)
#         bot.send_message(message.chat.id, "Пожалуйста, попробуйте ещё раз")

