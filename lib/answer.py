import random
from config import answers_bot

def answerBot(message):
    text = message.text.split()
    for answer in answers_bot:
        for word in text:
            # if you need to answer not every time
            # if (word in answer[0]) and (random.randrange(1,3) == 1):
            if (word in answer[0]):
                random.shuffle(answer[1])
                return answer[1][0] 
    return False