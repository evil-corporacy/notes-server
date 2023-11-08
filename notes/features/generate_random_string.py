import random
import string


def generate_random_string(length):
    characters = string.digits + string.ascii_letters
    result = ''.join(random.choice(characters) for _ in range(length))
    return result