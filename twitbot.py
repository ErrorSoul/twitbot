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

        #last mentions id
        self.m_id = 0 

        #list of time_of_days, when bot should update status
        self.time = [(4, 59), (17, 59), (19, 59)]
        

    def run_search(self, query, text):
        self.query = query
        try:
            result =  self.twitter.search(q=query)
        except TwythonError as e:
            print e 
        if result:
            

            #users = [(tweet id, user screen_name)]
            users = [(int(c["id"]), c["user"]["screen_name"])
                     for c in result["statuses"] if
                     (c["user"]["screen_name"] != u"ghohol" and
                      u"RT" not in c["text"])
                    ]
            
            ##retweets = self.my_reetwets()
            ##users = [x for x in users if x[0] not in retweets]
           
            #sorted tweets from older to younger
            users = sorted(users)
            print users
            
            print "#" * 30
            ## for user in users:
            ##     self.update_status(text,user)
            sleep(randint(60,240))
        else:
            pass 
            
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
                sleep(randint(180,400))
            except TwythonError as err:
                print err
                sleep(400)

    def show_status(self,*args, **kwargs):
        return self.twitter.show_status(*args, **kwargs)

    def update_dirty_status(self, name, id):
        answers = [ u"Ты еще и ругаешься",
                    u"Попросил бы без оскорблений",
                    u"Очень грубо",
                    u"Кто так обзывается, сам так называется",
                    u"Сколько мата тьфу ты бля"
                  ] 
              
        try:
            self.twitter.update_status(status= u"@{0} {1}".format(
                                       name, choice(answers)),
                                      in_reply_to_status_id=id)
            sleep(randint(140,260))
            
        except TwythonError as err:
            print err
            sleep (180)

 
    def retweet(self,id):
        try:
            self.twitter.retweet(id)
            sleep(randint(60,180))
        except TwythonError as e:
            print e
            sleep(120)
        
    def get_replays(self):
        dirty_list = [u"хуй", u"пидор",u"пидар", u"пидр",
                      u"бля", u"блядь", u"сука",u"ебень",
                      u"гондон", u"гандон", u"шлюха",
                      u"чмо", u"залупа", u"eблан",
                      u"козел", u"казел", u"козлина",
                      u"тварь", u"долбоеб", u"бандеровец",
                      u"блять", u"уеби", u"бендеровец"
                     ]
        
        

        def is_shit(tweet):
            t = tweet[2].lower()
            for word in dirty_list:
                if word in t:
                    return word
            return False
        since_id = self.m_id
        try:
            repl = self.twitter.get_mentions_timeline(include_rts = 0
                                                 )
            if repl:
                repl =[(c["id"],c["user"]["screen_name"],c["text"]) for c
                       in repl if u"RT" not in c["text"]]
                repl = filter(is_shit,repl)
                if repl:
                    for tw in repl:
                       ( self.retweet(tw[0]) if randint(0,1)
                         else self.update_dirty_status(tw[1],tw[0]))
                return repl 
        except TwythonError as err:
            print err
            sleep(360)
        return is_shit(tweet)
            



    
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
            ##     sleep(randint(1200,1800))
            ## except TwythonError as err:
            ##     print err
            ##     sleep(480)
        else:
            sleep(10)

class T_date(Thread):
    """Class for update status in certain time"""
    def __init__(self, twitter):
        Thread.__init__(self)
        self.twitter= twitter
    
    def run(self):
        while True:
            self.twitter.date_status(TEXT)
    
class D(Thread):
    def p(self):
        a = datetime.now()
        print "CURRENT TIME ==> {0}".format(a)
        sleep (6)
        
    def run(self):
        while True:
            self.p()
        

if __name__ == "__main__":
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    ## r = twitter.twitter.get_mentions_timeline(include_rts = 0, since_id = 391541784721256448)
    ## for tweet in r:
    ##     print 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['created_at'])
    ##     print "Tweet id %s" % (tweet['id'])
    ##     print tweet['text'].encode('utf-8'), '\n'
    
    y = twitter.get_replays()
    for c in y:
        print "Tweet from @{0} ID: {1}".format(c[1].encode('utf-8'), c[0])
        print c[2].encode('utf-8'), '\n'
    ## h = twitter.show_status(id=391313123053166592)
    ## for c in h:
    ##     print c,"=", h[c]
    ## a = twitter.my_reetwets()
    ## print a
    ## for c in a:
    ##     if u"хохол" in c[1]:
    ##         print c[1]
    ##         print "*" * 20
    ## d = D()
    ## d.daemon = True
    ## d.start()
    ## t = T_date(twitter)
    ## t.daemon = True
    ## t.start()
    ## while True:
    ##     #twitter.date_status(text)
    ##     for query in QUERYS:
    ##         twitter.run_search(query,replays)
    ##         sleep(480)
    ##     sleep(5)
