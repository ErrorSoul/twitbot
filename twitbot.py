#coding: utf-8

from twython import Twython, TwythonError 
from random import choice, randint 
from datetime import datetime
from threading import Thread
from time import time as t
from time import  sleep
from text import replays, night, afternoon, morning

CONSUMER_KEY       = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET    = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
OAUTH_TOKEN        = "1964645443-7XZiMnTEN0fp5e2CvuyYrsM8YralkeCfya6y2Th"
OAUTH_TOKEN_SECRET = "hcA1vYDtB5e3XVFHRzunNP5VBO0JBvxDGKeAIab3w"
QUERYS = [u"хахол", u"хохол"]
TEXT = [morning, afternoon, night]


class TwitBot(object):
    

    def __init__(self,c_key, c_secret,
                 o_token, o_token_secret):
        self.twitter = Twython(c_key, c_secret, o_token, o_token_secret)

        #last tweet id for query "xохол"
        self.id = [391240789764112385]

        #last tweet id for query "xахол"
        self.jd = [391091716893458433]

        #list of time_of_days, when bot should update status
        self.time = [(4, 59), (17, 59), (19, 59)]
        

    def run_search(self, query, text):
        self.query = query 
        result =  self.twitter.search(q=query)
        if result:
            

            #users = [(tweet id, user screen_name)]
            users = [(int(c["id"]), c["user"]["screen_name"])
                     for c in result["statuses"] if
                     (c["user"]["screen_name"] != u"ghohol" and
                      u"RT" not in c["text"])
                    ]
            
            retweets = self.my_reetwets()
            users = [x for x in users if x[0] not in retweets]
           
            #sorted tweets from older to younger
            users = sorted(users)
            print users
            
            print "#" * 30
            ## for user in s:
            ##     self.update_status(text,user)
            sleep(5)
            
    def update_status(self, text, user):
        q_id = self.id if self.query == u"хохол" else self.jd

        #replayed tweet or not 
        if  user[0] > q_id[0]:
            try:
                self.twitter.update_status(status= u"@{0} {1}".format(
                                           user[1], choice(text)),
                                           in_reply_to_status_id=user[0])
                #save last tweet id 
                q_id[0] = user[0]
                sleep(480)
            except TwythonError as err:
                print err
                sleep(400)

    def show_status(self,*args, **kwargs):
        return self.twitter.show_status(*args, **kwargs)



    
    def my_reetwets(self):
        """return id of my retweets"""

        retweets =  self.twitter.retweeted_of_me()
        retweets_id = [c["id"] for c in retweets]
        return retweets_id

    def get_followers_ids(self):
        return self.twitter.get_followers_ids()
    
    def date_status(self, text):
        current_time = datetime.now()
        print "current time = {0}".format(str(current_time))
        
        def part_of_day(time_of_day):
            """return True if current time equal time_of_day"""
            return (current_time.hour == time_of_day[0] and
                    current_time.minute in range(time_of_day[1]))

        check_time = filter(part_of_day, self.time)
        if check_time:
            print "check_time"
            sleep(10)
            ## message =  choice(text[self.time.index(s[0])])
            ## try:
            ##     self.twitter.update_status(status= u"{0}".format(message))
            ##     sleep(1200)
            ## except TwythonError as err:
            ##     print err
            ##     sleep(480)
        else:
            sleep(1000)

class T_date(Thread):
    """Class for update status in certain time"""
    def __init__(self, twitter):
        Thread.__init__(self)
        self.twitter= twitter
    
    def run(self):
        while True:
            self.twitter.date_status(TEXT)
    


if __name__ == "__main__":
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    
    ## h = twitter.show_status(id=391313123053166592)
    ## for c in h:
    ##     print c,"=", h[c]
    ## a = twitter.my_reetwets()
    ## print a
    ## for c in a:
    ##     if u"хохол" in c[1]:
    ##         print c[1]
    ##         print "*" * 20 
    ## t = T_date(twitter)
    ## t.daemon = True
    ## t.start()
    while True:
        #twitter.date_status(text)
        for query in QUERYS:
            twitter.run_search(query,replays)
    ##         sleep(480)
    ##     sleep(5)
