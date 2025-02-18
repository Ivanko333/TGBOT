import subprocess


def ping(host):
    res = subprocess.run(['ping', '-n', '1', host], stdout=subprocess.PIPE)
    return 'Сервер работает)' if res.returncode == 0 else "Сервер выключен :("


def check_bot(a):
    if a is None:
        return "Bot"
    else:
        return a


def send_debug(bot, id_chat, message):
    bot.send_message(id_chat,
                     f'Chat: {message.chat.id}({check_bot(message.chat.title)})\n'
                     f'Text: {message.text}\n'
                     f'From: {message.from_user.username}')
