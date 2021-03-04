# refactor DATA => GAME

import redis, os, datetime, math, random, telebot
from config import chat_id, master_id, members_count, emoji, answersBot, token
from lib.tools import extract_count
from mimesis import Person
# decorators
from lib.access import master, onlyTeam, adminTeam

r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
bot = telebot.TeleBot(token)
gen = Person('ru')

@adminTeam
def members(message):
    game = f'game_users{message.chat.id}'
    members = r.hgetall(game)
    if len(members) == 0:
        return 'Нет участников 😕'
    memberList = f'<strong>Сегодня играют:</strong> \n'
    i = 1
    for key in members:
        memberList += f'{i}. {key} : {members[key]}\n'
        i +=1
    return memberList


@adminTeam
def getGroups(message):
    game = f'game_users{message.chat.id}'

    counter_custom = extract_count(message.text)
    number = members_count
    if counter_custom > 2:
        number = counter_custom

    print("---------- getlist ----------------")
    print(r.hgetall(game))
    members = getList(r.hgetall(game))
    random.shuffle(emoji)
    count = len(members)
    if count<=5:
        return "🤷🏻‍♂️ Недостаточно участников"
    elif count<(number*2):
        group_count = 2
    elif count>=(number*2):
        group_count = math.floor(len(members)/number)
    groupList = '<b>Команды:</b>\n\n'
    gameGroups = [ [] for i in range(group_count)]
    k = 0
    for member in members:
        gameGroups[k].append(member[0])
        if k==group_count-1: 
            k = 0 
        else:
            k += 1

    print("---------- gameGroups ----------------")
    print(gameGroups)

def getList(gamers):
    return sorted(gamers.items(), key=lambda kv: kv[1])


@master
def setList(message):
    count = extract_count(message.text)
    game = f'game_users{message.chat.id}'
    for i in range(count):
        r.hset(game, gen.identifier('#########'), random.randrange(1,9))
    return 'List ready!'


@master
def delList(message):
    game = f'game_users{message.chat.id}'
    r.delete(game)
