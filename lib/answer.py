import random
from config import answersBot

def answerBot(message):
    text = message.text.split()
    for answer in answersBot:
        for word in text:
            if (word in answer[0]) and (random.randrange(1,3) == 1):
                random.shuffle(answer[1])
                return answer[1][0] 
    return False