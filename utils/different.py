__author__ = 'vwvolodya'
import random
import string


def generate_activation_key(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                   for _ in range(length))


if __name__ == '__main__':
    print generate_activation_key(64)
