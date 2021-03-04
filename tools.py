def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def getAdmin(message, bot):
    members = bot.get_chat_administrators(message.chat.id)
    list = []
    for member in members:
        list.append(member.user.id)
    return list

def extract_count(arg):
    try:
        return int(arg.split()[1])
    except:
        return 1