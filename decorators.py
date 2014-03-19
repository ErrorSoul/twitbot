#coding: utf-8
from twython import TwythonError
from time import sleep
from random import randint

def wrapper(n=120):
    def new(func):
        def shell(*args, **kwargs):
            try:
                f = func(*args, **kwargs)
                sleep(randint(n, 2*n))
                if f:return f
            except TwythonError as e:
                print e
                sleep(180)
        return shell
    return new

if __name__=="__main__":
    
    @wrapper(n=0)
    def x():
        return map(lambda x: x+1,range(10))
    print x()
