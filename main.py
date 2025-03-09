from telebot import *
import time
import random
import os
import options
import gpt
import secret


bot = TeleBot(secret.api)

debug = secret.debug
chanel = secret.chanel
chat_bot = secret.chat_bot
my_chat = secret.my_chat


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Привет, {message.from_user.first_name}")


@bot.message_handler(commands=['server'])
def send_ping(message):
    a = options.ping(secret.server)
    bot.reply_to(message, a)


@bot.message_handler(commands=['dior'])
def send_dior(message):
    num = random.randint(1, 4)

    if num == 1:
        video = open('/root/TGBOT/FILES/dior.mp4', 'rb')
        bot.send_video(message.chat.id, video)

    elif num == 2:
        photo = open('/root/TGBOT/FILES/dior1.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif num == 3:
        photo = open('/root/TGBOT/FILES/dior2.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif num == 4:
        photo = open('/root/TGBOT/FILES/dior3.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(message.chat.id, f"Поддержать автора:\nclck.ru/3GQWxZ", disable_web_page_preview=True)


@bot.message_handler(commands=['off'])
def off(message):
    bot.send_message(message.chat.id, "Размечтался...")


@bot.message_handler(content_types=['photo', 'audio', 'voice', 'sticker'])
def send_img(message):
    types = message.content_type
    if message.message_thread_id == 2978:
        if types == "photo":
            img = message.photo[-1].file_id
            bot.send_photo(my_chat, img)
        elif types == "audio":
            song = message.audio.file_id
            bot.send_voice(my_chat, song)
        elif types == "voice":
            voice = message.voice.file_id
            bot.send_voice(my_chat, voice)
        elif types == "sticker":
            stick = message.sticker.file_id
            bot.send_sticker(my_chat, stick)


@bot.message_handler(content_types=['text'])
def response(message):

    if message.message_thread_id == 2978:
        bot.send_message(my_chat, message.text)

    echo = message.text.split(" ")
    answer = "" # для CHATGPT в группе
    tell = "" # для "Сказать"
    sms = message.text.lower()
    boykisser = ['CAACAgIAAxkBAAENDl9nwx4_qphvCmndUCTkLgU4E462-AAC1j4AAtgvQUjO_bwr9IEtuTYE',
                 'CAACAgIAAxkBAAENDl1nwx39lPUzMKlGbgn05zTNFVMoawACB0oAAp5HYUtqPvNadgABVEA2BA',
                 'CAACAgIAAxkBAAENDmNnwx5vJJMlhXCZcAmkFJJ6XyBhqQACjEgAAkGMwEkOsFNNRoKOpTYE',
                 'CAACAgIAAxkBAAENDVlnwvWfdCUC0VNo1H0_ymeVtbWuxAACqTwAAh2WQUhFlySC_EiZYjYE',
                 'CAACAgIAAxkBAAENDmdnwx6ZTeVWpkf4gTCSrBnyEIdnuQACDz4AAi4BQEij3fesKj0GTjYE',
                 'CAACAgIAAxkBAAENDmlnwx6oq1RMZQtapfwhvz7iZTNQgAACFjUAAvk8QEiwBO0Inu7kozYE',
                 'CAACAgIAAxkBAAENDmtnwx60x5yr88U8Xkfq-40tGQg-RQACMUIAAsg5QUhxWEPrjEppATYE',
                 'CAACAgIAAxkBAAENDm1nwx7KV1KaTxQrEDrN_fRggP-RrQAC6TgAAgWVSEib-pPLVofo_DYE',
                 'CAACAgIAAxkBAAENDm9nwx7TAiI_CXUckvrzlJR4Hs9z7QACa0YAAi-CSEh2hKG3hS-hUzYE',
                 'CAACAgIAAxkBAAENDnFnwx7cNAlMSD9l2ZLXpaCOy5eCVQACkEAAAkZ-SUiu6Nl2Wm2GtTYE',
                 'CAACAgIAAxkBAAENDnNnwx7klfvXu7hJmGScEY0olLoOxQACkT8AAr6DSEicItGojW6eyDYE',
                 'CAACAgIAAxkBAAENDndnwx8I519Aqk1Se9HuuCMgcg7M5wAC_z0AAghgSEgNY3CP8anMdTYE',
                 'CAACAgIAAxkBAAENDodnwx-VUDj0EYm8o4rkxxnqgUix5gAC3j0AAq1HSEjZCRNzvmhHszYE',
                 'CAACAgIAAxkBAAENDolnwx-co8I1HEB_82_PT9fU8YWe0wAC_kQAAtcHSUhb7THSyCYNZDYE',
                 'CAACAgIAAxkBAAENDotnwx-mlC4J_y-yRiKLR2MfzLGDvQACLzoAAowBWEgsPrqaPlXYCTYE',
                 'CAACAgIAAxkBAAENDo1nwx-vHKLpqgABYHhW0ScK5XTBEmgAAldBAAIW1IBIvLRxNT-wOT82BA',
                 'CAACAgIAAxkBAAENDo9nwx-yHEFjHq73K9apqQ8vsxE8IwACXkQAAuE8gEgjTcW_gGgsojYE',
                 'CAACAgIAAxkBAAENDpNnwx_UodTy4bmJgonoHResLMlDygACS0gAAmij8UmFZdIozZOh6TYE',
                 'CAACAgIAAxkBAAENDpVnwx_aQ-H10SFSkvIc35TyrsPPJwACcz4AAi2GmEj3yTgk7ryaSDYE',
                 'CAACAgIAAxkBAAENDpdnwx_dBhynpPp5btWjZFe6JuNqFgACPk4AApHx2UrtlB29Ld_LQTYE',
                 'CAACAgIAAxkBAAENDplnwx_g-FA0mpNwtfmKgF_6gUMxcQACGFkAArEqCUlpPUmh_s7nuzYE',
                 'CAACAgIAAxkBAAENDptnwx_lSmeoUGsJ6XCbSxM1mf8vwAACQ1kAAsNWeUuRuvx5us5O2DYE'
                 'CAACAgIAAxkBAAENDp1nwx_nkjcJ3-TjcbH2mWMKPMjL4gACH2oAAmnjsUiT0auFtZtTsjYE',
                 'CAACAgIAAxkBAAENDVtnwvWvdSyaDHPRqbjs_Z2AfWZKXAACOT0AAqwkYUoKvpsIayF4gDYE']

    try:
        # если сообщения поступают не в диалоге с ботом
        if message.chat.type != 'private':

            if sms == "бот":
                bot.reply_to(message, "Работает!")

            if sms == "lol" or sms == "лол":
                bot.send_message(message.chat.id, 'Ага')

            if sms == "iann dior" or sms == "iann door" or sms == "iann" or sms == "ян диор" or sms == "диор":
                bot.reply_to(message, "Этот тот который nigga? 0_0")

            if sms == "топ":
                bot.reply_to(message, "Ты топ!")

            if sms == "ирис":
                bot.reply_to(message, "Жмот!")

            if sms == "кис кис" or sms == "кис-кис":
                bot.reply_to(message, "Мяу!")

            if sms == "кис кис кис":
                bot.reply_to(message, "ЖЕНЩИНА СЮРПРИЗ")

            if sms == "броен":
                bot.reply_to(message, "Я украла Брайна")

            if sms == "работает":
                bot.reply_to(message, "Конечно работаю))")

            if sms == "привет":
                bot.send_message(message.chat.id, "Ку ку")

            if sms == "хы" or sms == "хых":
                bot.send_message(message.chat.id, '😁')

            if sms == "telebot":
                bot.reply_to(message, "Да, это именна та библиотека, на которой я сделан)")

            if sms == ".api":
                bot.reply_to(message, message)

            if sms == "бу":
                bot.send_message(message.chat.id, "Бу! Испугался? Не бойся, я друг, я тебя не обижу. Иди сюда, иди ко мне, "
                                                  "сядь рядом со мной, посмотри мне в глаза."
                                                  "Ты видишь меня? Я тоже тебя вижу. Давай смотреть друг на друга до тех пор, "
                                                  "пока наши глаза не устанут. Ты не хочешь?"
                                                  "Почему? Что-то не так?")

            if sms == "ролл":
                bot.send_dice(message.chat.id, "🎲")
                time.sleep(2)

            if sms == "казино":
                bot.send_dice(message.chat.id, "🎰")
                time.sleep(2)

            if sms == "баскет":
                bot.send_dice(message.chat.id, "🏀")
                time.sleep(2)

            if sms == "бойкиссер":
                stick = random.choice(boykisser)
                bot.send_sticker(message.chat.id, stick)
                time.sleep(2)

            if echo[0].lower() == "скажи":
                for i in range(1, len(echo)):
                    tell += echo[i] + " "
                if echo[1:]:
                    bot.send_message(message.chat.id,
                                     f"{tell} \nОт: {message.from_user.first_name} (@{message.from_user.username})")


            # CHATGPT в группе
            elif echo[0].lower() == "спросить":
                for i in range(1, len(echo)):
                    answer += echo[i] + " "

                try:
                    if answer:
                        msg1 = bot.send_message(message.chat.id, "Бот думает. Ожидайте ответ в течениии 5-10 секунд")
                        bot.send_message(message.chat.id, gpt.ask(answer))
                        bot.delete_message(message.chat.id, msg1.message_id)
                    else:
                        bot.send_message(message.chat.id, "Вы ввели пустой запрос. Использование комманды: Спросить <сообщение>")

                except TypeError as e:
                    bot.reply_to(message, "Ошибка! Попробуйте ещё раз")
                    options.send_debug(bot, debug, 2977, e)
            # END

            for i in echo:
                if i.lower() == "волис":
                    bot.reply_to(message, "Волис ебётся с неграми...")
                break


        # CHATGPT в диалоге с ботом
        else:
            try:
                time.sleep(3)
                options.send_debug(bot, debug, 2977, message.from_user.username)
                bot.send_message(message.chat.id, gpt.ask(message.text))

            except Exception as e:
                bot.send_message(message.chat.id, "Пожалуйста, попробуйте ещё раз")
                options.send_debug(bot, debug, 2977, e)
        # END

    except Exception as e:
        options.send_debug(bot, debug, 2977, e)


if __name__ == "__main__":
    options.send_debug(bot, debug, 2977, "Бот включён")
    bot.infinity_polling()
    options.send_debug(bot, debug, 2977, "Бот выключен")

