import config
import telebot
import data

from lib.answer import answerBot
from lib.member import init as memberInit
import lib.game as game
from lib.get_members  import get_members


class MyBot(telebot.TeleBot):

    def __init__(self, token, **args):
        super().__init__(token, **args)

    def send_message(self, chat_id, text ):
        super().send_message(chat_id, text, parse_mode="HTML")


bot = MyBot(config.token)


@bot.message_handler(commands=['help',])
def initHelp(message):
    text = open('help.html', 'r')
    bot.send_message(message.chat.id, text.read())
    text.close()


@bot.message_handler(commands=['gamers',])
def getCool(message):
    list = game.members(message)
    print(list)
    game.getGroups(message)
    pass

@bot.message_handler(commands=['gcl',])
def glc(message):
    game.delList(message)
    print('======= Clear list! ========')
    pass

@bot.message_handler(commands=['getMembers','gm',])
def creatTeam(message):
    members = data.getMembersList(message)
    text = members if members else config.admin_text
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['group','gr',])
def getGroups(message):
    groups = data.getMembersGroups(message)
    text = groups if groups else config.admin_text
    bot.send_message(message.chat.id, text)   


@bot.message_handler(commands=['restart','rs',])
def clearBase(message):
    text = data.clearData(message) if data.clearData(message) else config.admin_text
    bot.send_message(message.chat.id, text)
    print('Clear!')


@bot.message_handler(commands=['tempMember','tm',])
def setMemberTemp(message):
    member = data.setMemberTemp(message)
    text = member if member else config.admin_text
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['kickMember','km',])
def clearMember(message):
    member = data.clearMember(message)
    text = member if member else config.admin_text
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['setlist','sl',])
def setList(message):
    result = data.setMemberList(message)
    text = result if result else config.admin_text
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def send_text(message):
    text = answerBot(message)
    # todo: remove!!!
    print('🦁 => Chat id!')
    print(message.chat.id)
    # end todo
    if message.text == '+':
        data.setMember(message)
        # new add
        member = memberInit(message)
        member.inGame()
    elif message.text == '-': 
        data.delMember(message)
        # new add
        member = memberInit(message)
        member.outGame()
    if text: 
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop = True)