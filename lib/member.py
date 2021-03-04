import redis, os, datetime

import config
from lib.access import master, onlyTeam, getAdmin

r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)


class Member:
    def __init__(self, chat, id):
        self.chat = f'users{chat}'
        self.id = id
        r.hsetnx(self.chat, self.id, 0)
        self.skill = int(r.hget(self.chat,self.id))

    def skillUp(self):
        skill = int(r.hget(self.chat,self.id))
        r.hset(self.chat, self.id, skill+1)
    
    def skillDown(self):
        skill = int(r.hget(self.chat,self.id))
        if skill > 0:
            r.hset(self.chat, self.id, skill-1)
    
    def inGame(self):
        game = f'game_{self.chat}'
        user_id = f'{self.id}'
        user_skill = f'{self.skill}'
        r.hset(game, user_id, user_skill)
        r.expire(game, datetime.timedelta(hours=24))
        return True

    def outGame(self):
        game = f'game_{self.chat}'
        user_id = f'{self.id}'
        r.hdel(game, user_id)
        

@onlyTeam
def init(message):
    return Member(message.chat.id, message.from_user.id)
    # member.skillUp()
    # return True

