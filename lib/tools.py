import telebot
from config import chat_id, token

bot = telebot.TeleBot(token)


def getAdmin(chat_id):
    admin_list = bot.get_chat_administrators(chat_id)
    admins = []
    for admin in admin_list:
        admins.append(admin.user.id)
    return admins

def extract_count(arg):
    try:
        return int(arg.split()[1])
    except:
        return 1