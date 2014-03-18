from threading import Thread 
from twython import Twython
from twython import TwythonStreamer
import time 

CONSUMER_KEY = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
oauth_token_secret = '1uZiuWCXwE78og5SHGhz85opeAIqoyskNPT3OeHftlfnO'
oauth_token='74446564-IasJQxyO7JzgnbRhyl5bamFQSzUwQDG4LB68KHjqZ'


## class MyStreamer(TwythonStreamer):
##     def x(self, gen):
##         self.generator = gen()

##     def terminator(self):
##         time.sleep(2)
##         c = 0 
##         while c < 100000:
##             print c
##             if c == 50000:
##                 self.connected=False
##             c += 1
        
##     def on_success(self, data):
        
        
       
##         if 'text' in data:
##             print (data['text'].encode('utf-8'))
##         if not self.connected:
##             print "ssssssssssss"

##     def on_error(self, status_code, data):
##         print status_code

##     def run(self):
##         self.user()
##         print "Hleb"
##         self.disconnect()
## stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret,timeout=300)
## def gena():
    
##     while True:
##         x = yield a
##         print x 
## t = Thread(target=stream.user)
## t.start
## #stream.x(gena)
## #stream.generator.next()
## stream.user()

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret)
f = twitter.show_status(id="423392305043615744")
a =  twitter.show_status(id="423392936773308416")
for a,b in a.iteritems():
    print a, '->>>>', b

for a,b in f.iteritems():
    print a, '-----<>', b

def gen_tweet(max_id=422465648254390272, count=200):
    d = twitter.get_user_timeline(max_id=max_id, count=count)
    tweets = (tw for tw in d)
    tw_number = ((t[0], t[1]["id"], t[1]["in_reply_to_screen_name"]) for t in enumerate(tweets))

    last_tweet = (t[1] if t[0]==186 else 5 for t in tw_number if t[2])
    return last_tweet
    ## for c in tw_number:
    ##     if c[0]==189:
    ##         yield c[0]
    ##     else:
    ##         if c[1]:
    ##             yield 5 
            
    
    
## In [31]: d = {True:lambda x: x + 1, False: lambda x: x*2}

## In [32]: z = (c if c>7 else d[c%2==0](c) for c in range(10))
   
