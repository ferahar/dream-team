# REMOVE after refactor DATA => GAME
import redis, os, datetime, math, random

from config import chat_id, master_id, members_count, emoji, answersBot
from bot import bot
from mimesis import Person

gen = Person('ru')
r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

# decorators refactor to => access.py
def master(f):
    def wrapper(message, *args, **keyargs):
        if message.from_user.id in master_id:
            return f(message, *args, **keyargs)
        else:
            return False
    return wrapper

def adminTeam(f):
    def wrapper(message, *args, **keyargs):
        admin_list = bot.get_chat_administrators(message.chat.id)
        if message.from_user.id in getAdmin(admin_list):
            return f(message, *args, **keyargs)
        else:
            return False
    return wrapper

def adminTeam2(admin_list):
    def wrapOut(f):
        def wrapper(message, *args, **keyargs):
            if message.from_user.id in getAdmin(admin_list):
                return f(message, *args, **keyargs)
            else:
                return False
        return wrapper
    return wrapOut

def onlyTeam(f):
    def wrapper(message, *args, **keyargs):
        if message.chat.id in chat_id:
            return f(message, *args, **keyargs)
        else:
            return False
    return wrapper

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def getAdmin(members):
    list = []
    for member in members:
        list.append(member.user.id)
    return list

def extract_count(arg):
    try:
        return int(arg.split()[1])
    except:
        return 1

@onlyTeam
def setMember(message):
    chat = f'chat{message.chat.id}'
    user_id = f'{message.from_user.id}'
    user_name = f'{message.from_user.first_name}'
    user_name += f' {message.from_user.last_name}' if message.from_user.last_name else ""
    user_name += f' ({message.from_user.username})' if message.from_user.username else ""
    r.hset(chat, user_id, user_name)
    r.expire(chat, datetime.timedelta(hours=24))
    return True

@onlyTeam
def delMember(message):
    chat = f'chat{message.chat.id}'
    user_id = f'{message.from_user.id}'
    r.hdel(chat, user_id)

@adminTeam
def getMembersGroups(message):
    chat = f'chat{message.chat.id}'
    counter_custom = extract_count(message.text)
    number = members_count
    if counter_custom > 2:
        number = counter_custom
    members = r.hvals(chat)
    random.shuffle(members)
    random.shuffle(emoji)
    count = len(members)
    if count<=5: 
        return "🤷🏻‍♂️ Недостаточно участников " 
    elif count<(number*2):
        group_count = 2
        members_c = math.floor(len(members)/2)
    elif count>=(number*2):
        group_count = math.floor(len(members)/number)
        members_c = number

    groupList = '<b>Команды:</b>\n\n'

    for i in range(group_count):
        groupList += f'{emoji[i]} <strong>Group #{i+1}:</strong> \n'
        for m in range(members_c):
            if len(members):
                groupList += f'{m+1}. {members[0]}\n'
                del members[0]
        groupList += f'\n'

    if len(members):
        groupList += f'👶🏼 <strong>Elite commando</strong> \n'
        for member in members:
            groupList += f'{member}\n'

    return groupList


@adminTeam
def getMembersList(message):
    chat = f'chat{message.chat.id}'
    members = r.hgetall(chat)
    if len(members)==0:
        return 'Нет участников 😕'
    memberList = f'<strong>Участники игры:</strong> \n'
    i = 1
    for key in members:
        memberList += f'{i}. {members[key]}\n'
        i +=1
    return memberList


@adminTeam
def setMemberTemp(message):
    chat = f'chat{message.chat.id}'
    try:
        name = message.text.split()[1]
    except:
        name = gen.name()

    user_id = gen.identifier('###')
    name = name + '(/km '+ user_id + ')'
    r.hset(chat, user_id, name)
    return f'{name} id={user_id}, \nудалить {name} /km {user_id}'

@adminTeam
def clearMember(message):
    chat = f'chat{message.chat.id}'
    try:
        key = message.text.split()[1]
        # name = message.text.split()[2]
        r.hdel(chat,key)
    except:
        return 'Участник не найден'
    return f'Участник удален'


@master
def clearData(message):
    chat = f'chat{message.chat.id}'
    r.delete(chat)
    return "Ok 👍🏻"


# for do
@master
def setMemberList(message):
    count = extract_count(message.text)
    chat = f'chat{message.chat.id}'
    for i in range(count):
        r.hset(chat, gen.identifier('########'), gen.full_name())
        i
    return 'List ready!'