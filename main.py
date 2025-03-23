from telebot import *
import time
import random
import options
import gpt
import secret
import stickers


bot = TeleBot(secret.api)

debug = secret.debug
chat_bot = secret.chat_bot
my_chat = secret.my_chat
I = secret.I
svet = secret.svet
status = True


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.text == "/start@IvanSkyBot" and message.chat.type != 'private':
        bot.reply_to(message, f"Привет, {message.from_user.first_name}")
    else:
        bot.reply_to(message, f"Привет, {message.from_user.first_name}")


@bot.message_handler(commands=['qrgen', 'genqr'])
def qr(message):
    try:
        text = message.text.split(' ')
        gpt.generate_qr(message, text[1])
    except IndexError:
        bot.reply_to(message, "Ошибка. Использование команды: /link текст или ссылка которую надо сгенерировать")


@bot.message_handler(commands=['link'])
def link_shot(message):
    url = message.text.split(' ')
    try:
        gpt.link(message, url[1])
    except IndexError:
        bot.reply_to(message, "Ошибка. Использование команды: /link ссылка")


@bot.message_handler(commands=['setstatus'])
def work(message):
    global status
    text = message.text.split(' ')

    if message.from_user.id == I:
        if text[1] == "True":
            status = True

        elif text[1] == "False":
            status = False


@bot.message_handler(commands=['dior'])
def send_dior(message):
    options.random_dior(message.chat.id)


@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(message.chat.id, f"Поддержать автора:\nclck.ru/3GQWxZ", disable_web_page_preview=True)


@bot.message_handler(commands=['git', 'github'])
def git(message):
    bot.send_message(message.chat.id, "Вот сыллка на мой код: clck.ru/3HCoes", disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def response(message):

    echo = message.text.split(" ")
    answer = "" # для CHATGPT в группе
    sms = message.text.lower()

    try:
        # если сообщения поступают не в диалоге с ботом
        if message.chat.type != 'private':

            if sms == "бот":
                bot.reply_to(message, "Работает!")

            if sms == "lol" or sms == "лол":
                bot.send_message(message, 'Хвхахвахав')

            if sms == "iann dior" or sms == "iann door" or sms == "iann" or sms == "ян диор" or sms == "диор" or sms == "dior":
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
                bot.send_message(message.chat.id, "Приветики)")

            if sms == "хы" or sms == "хых" or sms == "хех" or sms == "хехе" or sms == "хе":
                bot.send_message(message.chat.id, '😁')

            if sms == "telebot":
                bot.reply_to(message, "Да, это именна та библиотека, на которой я сделан)")

            if sms == ".api" and message.from_user.id == secret.I:
                bot.reply_to(message, message)

            if sms == "бу":
                bot.send_message(message.chat.id, "Бу! Испугался? Не бойся, я друг, я тебя не обижу. Иди сюда, иди ко мне, "
                                                  "сядь рядом со мной, посмотри мне в глаза."
                                                  "Ты видишь меня? Я тоже тебя вижу. Давай смотреть друг на друга до тех пор, "
                                                  "пока наши глаза не устанут. Ты не хочешь?"
                                                  "Почему? Что-то не так?")

            if sms == "ролл":
                bot.send_dice(message.chat.id, "🎲")

            if sms == "казино" or sms == "рулетка":
                bot.send_dice(message.chat.id, "🎰")

            if sms == "баскет":
                bot.send_dice(message.chat.id, "🏀")

            if sms == "бойкиссер":
                stick = random.choice(stickers.boykisser)
                bot.send_sticker(message.chat.id, stick)


            if message.text.lower().startswith("бот скажи"):
                for i in range(2, len(echo)):
                    answer += echo[i] + " "

                if echo[1:]:
                    bot.send_message(message.chat.id, f"{answer} \nСказал: {message.from_user.first_name}")


            if message.text.lower().startswith("шар"):
                words = ["Да", "Частично", "Хз", "Нет", "Не совсем", "100%"]
                if len(echo) > 1:
                    response = random.choices(words, weights=[18, 19, 20, 17, 21, 14], k=1)[0]
                    bot.reply_to(message, f"🔮 {message.from_user.first_name}, Я думаю: *{response}*", parse_mode='MarkdownV2')
                else:
                    bot.send_message(message.chat.id, "Вы не ввели текст. Использование: Шар <Текст>")


            # CHATGPT в группе
            if message.text.lower().startswith("@ivanskybot"):
                if status:
                    for i in range(1, len(echo)):
                        answer += echo[i] + " "

                    try:
                        if answer:
                            msg1 = bot.send_message(message.chat.id, "Бот думает. Ожидайте ответ в течениии 5-10 секунд")
                            gpt.start_gpt(message, answer)
                            time.sleep(3)
                            bot.delete_message(message.chat.id, msg1.message_id)

                        else:
                            bot.send_message(message.chat.id, "Вы ввели пустой запрос. Использование комманды: Спросить <сообщение>")

                    except Exception as e:
                        bot.reply_to(message, "Ошибка! Попробуйте ещё раз")
                        options.send_debug(debug, 2977, e)
                else:
                    bot.send_message(message.chat.id, "Бот находится на тех обслуживании")
            # END


        # CHATGPT в диалоге с ботом
        else:
            if status:
                try:
                    options.send_debug(debug, 2977, f"@{message.from_user.username}({message.from_user.id})")
                    gpt.start_gpt(message, message.text)

                except Exception as e:
                    bot.send_message(message.chat.id, "Пожалуйста, попробуйте ещё раз")
                    options.send_debug(debug, 2977, e)
            else:
                bot.send_message(message.chat.id, "Бот находится на тех обслуживании")
        # END

    except Exception as e:
        options.send_debug(debug, 2977, e)



if __name__ == "__main__":
    options.start_time(svet)
    gpt.potok()
    options.send_debug(debug, 2977, "Бот включён")
    bot.infinity_polling()
    options.send_debug(debug, 2977, "Бот выключен")

