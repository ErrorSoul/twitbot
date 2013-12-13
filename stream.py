from threading import Thread 
from twython import Twython
from twython import TwythonStreamer
import time 

CONSUMER_KEY = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
oauth_token_secret = '1uZiuWCXwE78og5SHGhz85opeAIqoyskNPT3OeHftlfnO'
oauth_token='74446564-IasJQxyO7JzgnbRhyl5bamFQSzUwQDG4LB68KHjqZ'


class MyStreamer(TwythonStreamer):
    def x(self, gen):
        self.generator = gen()

    def terminator(self):
        time.sleep(2)
        c = 0 
        while c < 100000:
            print c
            if c == 50000:
                self.connected=False
            c += 1
        
    def on_success(self, data):
        
        
       
        if 'text' in data:
            print (data['text'].encode('utf-8'))
        if not self.connected:
            print "ssssssssssss"

    def on_error(self, status_code, data):
        print status_code

    def run(self):
        self.user()
        print "Hleb"
        self.disconnect()
stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret,timeout=300)
def gena():
    
    while True:
        x = yield a
        print x 
t = Thread(target=stream.user)
t.start
#stream.x(gena)
#stream.generator.next()
stream.user()

