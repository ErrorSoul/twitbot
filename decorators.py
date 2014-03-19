#coding: utf-8
from twython import TwythonError
from time import sleep
from random import randint

def wrapper(func):
    def shell(*args, **kwargs):
        try:
            f = func(*args, **kwargs)
            sleep(randint(120, 240))
            if f:return f
        except TwythonError as e:
            print e
            sleep(180)
    return shell


