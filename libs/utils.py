import hashlib
import time


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