import hashlib
import time
import random
import string


def encrypt(password):
    m = hashlib.md5()
    m.update(password)
    m.update(" the spammish repetition")
    return m.hexdigest()


def createHash():
    """This function generate 10 character long hash"""
    _hash = hashlib.sha1()
    _hash.update(str(time.time()))
    return _hash.hexdigest()


def generate_activation_key(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                   for _ in range(length))


if __name__ == '__main__':
    print generate_activation_key(64)