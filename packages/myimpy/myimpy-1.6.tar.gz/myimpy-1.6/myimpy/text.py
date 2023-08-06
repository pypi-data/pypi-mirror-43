import random

def greet():
    return ('I AM HERE.')

def why():
    why_list = ['Because the smart jinhang wants to make a difference.',
        'Could you just please ask another question?',
        'Deep night can always make me bloody perky',
        'Ask Kojo and he may know']
    index = random.randint(0,len(why_list) - 1)
    return why_list[index]