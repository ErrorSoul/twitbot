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
        self.id = [391240789764112385]
        self.jd = [391091716893458433]
        self.time = [(4, 59), (13, 59), (19, 59)]

    def run_search(self, query, text):
        self.query = query 
        result =  self.twitter.search(q=query)
        if result:
           
            s = [(int(c["id"]), c["user"]["screen_name"]) for c in result["statuses"]]
            s = sorted(s)
            print s
            for user in s:
                self.update_status(text,user)
            sleep(300)

    def update_status(self, text, user, q_id):
        q_id = self.id if self.query == u"хохол" else self.jd
         if user[1] != u"ghohol" and user[0] > q_id[0]:
            try:
                self.twitter.update_status(status= u"@{0} {1}".format(
                                           user[1], choice(text)),
                                           in_reply_to_status_id=user[0])
                q.id[0] = user[0]
                sleep(480)
            except TwythonError as err:
                print err
                sleep(400)

    def date_status(self, text):
        current_time = datetime.now()
        def part_of_day(a):
            return current_time.hour == a[0] and current_time.minute in range(a[1])
        s = filter(part_of_day,self.time)
        if s:
            message =  choice(text[self.time.index(s[0])])
            try:
                self.twitter.update_status(status= u"{0}".format(message))
                sleep(360)
            except TwythonError as err:
                print err
                sleep(280)


if __name__ == "__main__":
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    while True:
        twitter.date_status(text)
        for c in g:
            twitter.run_search(c,replays)
            sleep(480)
        sleep(500)
