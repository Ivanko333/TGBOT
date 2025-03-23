from telebot import *
import datetime
import time
import threading
import secret
import os

bot = TeleBot(secret.api)


def send_debug(chat_id, topic_id, message_text):
    bot.send_message(chat_id=chat_id, message_thread_id=topic_id, text=message_text)


def check_time(chat_id):
    while True:
        now = datetime.datetime.now()
        if (now.weekday() == 0 and now.time().hour == 17 and now.time().minute == 0) or (now.weekday() == 2 and now.time().hour == 17 and now.time().minute == 0):
            bot.send_message(chat_id, "Тренировка")
        time.sleep(60)


def start_time(chat_id):
    thread = threading.Thread(target=check_time, args=(chat_id,))
    thread.daemon = True
    thread.start()

def random_dior(chat_id):
    dior = ['/root/TGBOT/FILES/dior.mp4', '/root/TGBOT/FILES/dior1.jpg', '/root/TGBOT/FILES/dior2.jpg', '/root/TGBOT/FILES/dior3.jpg', "/root/TGBOT/FILES/dior4.jpg"]
    choice = random.choices(dior, weights=[15, 20, 21, 22, 19], k=1)[0]
    extension = choice.split('.')
    if extension == "mp4":
        video = open(choice, 'rb')
        bot.send_video(chat_id, video)
    else:
        photo = open(choice, 'rb')
        bot.send_photo(chat_id, photo)

