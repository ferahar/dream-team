import redis, os

import config
from lib.access import master, onlyTeam, adminTeam

r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

@adminTeam
def get_members(message):
    chat = f'users{message.chat.id}'
    members = r.hgetall(chat)
    return members