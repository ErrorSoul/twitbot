#coding: utf-8

from twython import Twython, TwythonError 
from random import choice
from datetime import datetime
from time import sleep
from text import replays, night, afternoon, morning

CONSUMER_KEY       = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET    = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
OAUTH_TOKEN        = "1964645443-7XZiMnTEN0fp5e2CvuyYrsM8YralkeCfya6y2Th"
OAUTH_TOKEN_SECRET = "hcA1vYDtB5e3XVFHRzunNP5VBO0JBvxDGKeAIab3w"


g = [u"хахол", u"хохол"]

   

text = [morning, afternoon, night]


class TwitBot(object):
    def __init__(self,c_key, c_secret,
                 o_token, o_token_secret):
        self.twitter = Twython(c_key, c_secret, o_token, o_token_secret)
        self.id = 0
        self.time = [(4, 10), (13, 10), (19, 10)]

    def run_search(self, query, text):
        result =  self.twitter.search(q=query)
        if result:
           
            s = [(int(c["id"]), c["user"]["screen_name"]) for c in result["statuses"]]
            s = sorted(s)
            print s
            for user in s:
                self.update_status(text,user)
            sleep(200)

    def update_status(self, text, user):
         if user[0] > self.id:
            try:
                self.twitter.update_status(status= u"@{0} {1}".format(
                                           user[1], choice(text)),
                                           in_reply_to_status_id=user[0])
                self.id = user[0]
                sleep(20)
            except TwythonError as err:
                print err
                sleep(40)

    def date_status(self, text):
        current_time = datetime.now()
        def part_of_day(a):
            return current_time.hour == a[0] and current_time.minute in range(a[1])
        s = filter(part_of_day,self.time)
        if s:
            message =  choice(text[self.time.index(s[0])])
            try:
                self.twitter.update_status(status= u"{0}".format(message))
                sleep(60)
            except TwythonError as err:
                print err
                sleep(60)


if __name__ == "__main__":
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    while True:
        twitter.date_status(text)
        for c in g:
            twitter.run_search(c,replays)
            sleep(30)
        sleep(30)
