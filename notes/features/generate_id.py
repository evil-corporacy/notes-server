import random
import string


def generate_id():
    characters = string.digits + string.ascii_letters
    result = ''.join(random.choice(characters) for _ in range(32))
    return result
