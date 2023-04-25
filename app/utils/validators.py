import string

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGIT = string.digits
SYMBOL = string.punctuation
MIN_LENGTH = 12
MAX_LENGTH = 32


def _check_char(char, iterables):
    for iterable in iterables:
        if char in iterable:
            iterables.remove(iterable)
            break

    return iterables


def password_is_valid(password):
    if len(password) < MIN_LENGTH or len(password) > MAX_LENGTH:
        return False
    iterables = [LOWER, UPPER, DIGIT, SYMBOL]
    for char in password:
        if not iterables:
            break
        iterables = _check_char(char, iterables)
    return not iterables
