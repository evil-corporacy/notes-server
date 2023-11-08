import re


def check_cyrillic(string):
    pattern = re.compile('[А-Яа-я]')
    return bool(pattern.search(string))
