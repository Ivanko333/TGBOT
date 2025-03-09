import subprocess


def ping(host):
    res = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
    return 'Сервер работает)' if res.returncode == 0 else "Сервер выключен :("


def ping1(host):
    res = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
    return res


def send_debug(bot, chat_id, topic_id, message_text):
    bot.send_message(chat_id=chat_id, message_thread_id=topic_id, text=message_text)
