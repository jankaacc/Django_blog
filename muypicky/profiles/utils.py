
import random
import string

def code_generator(size):
    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
    return randstr