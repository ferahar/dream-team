# decorators
import telebot
from config import chat_id, master_id, token
from lib.tools import getAdmin

bot = telebot.TeleBot(token)

def master(f):
    def wrapper(message, *args, **keyargs):
        if message.from_user.id in master_id:
            return f(message, *args, **keyargs)
        else:
            return False
    return wrapper
    

def adminTeam(f):
    def wrapper(message, *args, **keyargs):
        if message.from_user.id in getAdmin(message.chat.id):
            return f(message, *args, **keyargs)
        else:
            return False
    return wrapper


def onlyTeam(f):
    def wrapper(message, *args, **keyargs):
        if message.chat.id in chat_id:
            return f(message, *args, **keyargs)
        else:
            return False
    return wrapper
