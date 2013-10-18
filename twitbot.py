#coding: utf-8

from twython import Twython, TwythonError 
from random import choice
from time import sleep

CONSUMER_KEY       = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET    = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
OAUTH_TOKEN        = "1964645443-7XZiMnTEN0fp5e2CvuyYrsM8YralkeCfya6y2Th"
OAUTH_TOKEN_SECRET = "hcA1vYDtB5e3XVFHRzunNP5VBO0JBvxDGKeAIab3w"

## twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,
##                   OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

g = u"Джульга"
#twitter.update_status(status='See how easy using Twython is!')
## t=  twitter.search(q=g)
## s = [(int(c["id"]), c["user"]["screen_name"]) for c in t["statuses"]]
## print sorted(s)
## for c in s:
##     twitter.update_status(status=u"@%s Что за\n хуйня " %
##                           c[1],
##                           in_reply_to_status_id = c[0] )
    

##     for d in c:
##         id = c["id"]
##         user = c["user"]
##         ## twitter.update_status(status=u"@%s Что за хуйня " %
##         ##                       user["screen_name"],
##         ##                       in_reply_to_status_id = id )
##     print user["screen_name"]
##     print id 
##             #print d + " = " , c[d]  

##         #print c,"\n"
##     print "########################"
   
text = [u'что за хрень?' , u"ишь чо выдумал?", u"ты чо пидорас? "]


class TwitBot(object):
    def __init__(self,c_key, c_secret,
                 o_token, o_token_secret):
        self.twitter = Twython(c_key, c_secret, o_token, o_token_secret)
        self.id = 0 

    def run_search(self, query, text):
        result =  self.twitter.search(q=query)
        if result:
            s = [(int(c["id"]), c["user"]["screen_name"]) for c in result["statuses"]]
            s = sorted(s)
            for user in s:
                self.update_status(text,user)
            sleep(60)

    def update_status(self, text, user):
         if user[0] > self.id:
            try:
                self.twitter.update_status(status= u"@{0} {1}".format(
                                           user[1], choice(text)),
                                           in_reply_to_status_id=user[0])
                self.id = user[0]
                sleep(10)
            except TwythonError as err:
                print err
                sleep(20)


if __name__ == "__main__":
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    twitter.run_search(g,text)
    
