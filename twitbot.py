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
        self.id = [0]

        #last tweet id for query "xахол"
        self.jd = [0]

        #last mentions id
        self.m_id = 0

        #last timelines tweet id
        self.t_id = 0

        #list of time_of_days, when bot should update status
        self.time = [(4, 59), (17, 59), (19, 59)]

        #count of replies of day
        self.replies_count = 35
        self.flag = True
        
    
    def get_users(self, result, debug = 0):
        #users = [(tweet id, user screen_name)]
        users = [(int(c["id"]), c["user"]["screen_name"])
                 for c in result["statuses"] if
                 (c["user"]["screen_name"] != u"ghohol" and
                 u"ghohol" not in c["text"])
                ]
            
        retweets = self.my_reetwets()
        users = [x for x in users if x[0] not in retweets]
           
        #sorted tweets from older to younger
        users = sorted(users)
        if not debug:
            print users
            print "#" * 40,'\n'
        return users
##################################RUN SEARCH############################################        
    def run_search(self, query, text):
        self.query = query
        try:
            result =  self.twitter.search(q=query)
        except TwythonError as e:
            print e

        if result:
            users = self.get_users(result)

            if replies_count < 31:
                
                for user in users:
                    self.update_status(text,user)
                    replies_count +=1
                sleep(randint(180,440))
        else:
            sleep(randint(240, 480))
            
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
                sleep(randint(200,400))
            except TwythonError as err:
                print err
                sleep(400)
################################################################################
    def show_status(self,*args, **kwargs):
        return self.twitter.show_status(*args, **kwargs)

    def update_dirty_status(self, name, id):
        answers = [ u"Ты еще и ругаешься",
                    u"Попросил бы без оскорблений",
                    u"Очень грубо",
                    u"А можно без мата?",
                    u"Кто так обзывается, сам так называется",
                    u"Сколько мата тьфу ты, бля"
                  ] 
              
        try:
            self.twitter.update_status(status= u"@{0} {1}".format(
                                       name, choice(answers)),
                                      in_reply_to_status_id=id)
            sleep(randint(140,280))
            
        except TwythonError as err:
            print err
            sleep (280)

   
################################HOME TIMELINE######################################
    def home_timeline(self):
        hour = datetime.now().hour
        if hour == 17 and self.flag:
                self.replies_count = 0
                self.flag = False
        if (hour in range(0,3) or range(9,24)
            and hour % 4 == 0):
            
                
            print "CHECK TIMELINE UPDATES"
            try:
                 result = self.twitter.get_home_timeline(count= 30,exclude_replies = 1,
                                                         since_id = self.t_id)
                 tw = [tweet["id"] for tweet in result if tweet['user']['screen_name'] != u"ghohol"]
                 self.t_id = tw[0]
                 if randint(0,7) == 3:
                     map(self.retweet, filter(lambda x:x % 7 == 0, tw))

                 if randint(0,7) == 3:
                     map(self.favorite, filter(lambda x: x%5 == 0, tw))
                 #this part for debug (delete)
                 for tweet in result:
                     print 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['created_at'])
                     print "Tweet id %s" % (tweet['id'])
                     print tweet['text'].encode('utf-8'),'\n'
                 sleep(300)
            except TwythonError as err:
                print err
                sleep(300)
        else:
            print "NO TIMELINE UPDATES"

################################################################################

    def retweet(self, id):
        try:
            self.twitter.retweet(id=id)
            sleep(randint(60,180))
        except TwythonError as e:
            print e
            sleep(120)

    def favorite(self, id):
        try:
            self.twitter.create_favorite(id=id)
            sleep(randint(45,100))
        except TwythonError as err:
            print err
            sleep(180)

    def delete_status(self, id):
        try:
            self.twitter.destroy_status(id=id)
            sleep(randint(200,480))
        except TwythonError as e:
            print e
            sleep(120)

###############################GET REPLAYS#############################################

    def get_replays(self):
        dirty_list = [u"хуй", u"пидор",u"пидар", u"пидр",
                      u"бля", u"блядь", u"сука",u"ебень",
                      u"гондон", u"гандон", u"шлюха",
                      u"чмо", u"залупа", u"eблан",
                      u"козел", u"казел", u"козлина",
                      u"тварь", u"долбоеб", u"бандеровец",
                      u"блять", u"уеби", u"бендеровец",
                      u"дебил", u"дибил", u"петух",
                      u"питух", u"петушок"
                     ]
        
        

        def is_shit(tweet):
            t = tweet[2].lower()
            for word in dirty_list:
                if word in t:
                    return word
            return False
        
        try:
            repl = self.twitter.get_mentions_timeline(include_rts = 0,
                                                      since_id = self.m_id)

            if repl:
                repl =[(c["id"],c["user"]["screen_name"],c["text"]) for c
                       in repl if u"RT" not in c["text"]]
                self.m_id = repl[0][0]
                repl = filter(is_shit, repl)
                if repl:
                    for tw in repl:
                       (self.retweet(tw[0]) if randint(0,1)
                        else self.update_dirty_status(tw[1],tw[0]))
                return repl
            return repl 
        except TwythonError as err:
            print err
            sleep(360)
        
            

########################################START########################################

    def start(self):
        def complete(attr):
            d = {"self.jd":self.jd, "self.id":self.id,
                 "self.t_id":self.t_id, "self.m_id":self.m_id}
            print "##### COMPLETE #####\n"
            print "{0} = {1} {2} complete\n".format(attr, d[attr],'.' * 25)

        while ((not self.m_id or not self.t_id) or
               (self.id[0] == 0 or self.jd[0] == 0)):
            try:
                for query in QUERYS:
                    result = self.twitter.search(q=query)
                    if query == u"хахол":
                        self.jd[0] = self.get_users(result,debug=1)[-1][0]
                        if self.jd[0]:
                            complete("self.jd")
                           
                    else:
                        self.id[0] = self.get_users(result,debug=1)[-1][0]
                        if self.id[0]:
                            complete("self.id")
                            
                self.t_id = self.twitter.get_home_timeline(exclude_replies = 1)[0]["id"]
                if self.t_id:
                    complete("self.t_id")

                self.m_id =  self.twitter.get_mentions_timeline(count=30, include_rts = 0)[0]["id"]
                if self.m_id:
                    complete("self.m_id")
                
            except TwythonError as err:
                print err
                sleep(480)
####################################################################################                    
        
    def my_reetwets(self):
        """return id of my retweets"""

        retweets =  self.twitter.retweeted_of_me()
        retweets_id = [c["id"] for c in retweets]
        return retweets_id

    def get_followers_ids(self):
        return self.twitter.get_followers_ids()

    def delete_replies(self):
        a = datetime.now().hour
        if a == 22:
            print "START CLEAR TWEETS"
            try:
                tweets = self.twitter.get_user_timeline(count= 100)
                tweets = [c["id"] for c in tweets if c["in_reply_to_user_id"] ]
                sleep(15)
                map(self.delete_status, tweets)
            except TwythonError as err:
                print err
                sleep(randint(125, 200))
        else:
            print "NO CLEAN"
                
###############################DATE STATUS############################################

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
            message =  choice(text[self.time.index(check_time[0])])
            try:
                self.twitter.update_status(status= u"{0}".format(message))
                sleep(randint(1200,1800))
            except TwythonError as err:
                print err
                sleep(480)
        else:
            sleep(randint (1200,1800))

################################################################################
class T_date(Thread):
    """Class for update status in certain time"""
    def __init__(self, twitter):
        Thread.__init__(self)
        self.twitter= twitter
    
    def run(self):
        while True:
            self.twitter.date_status(TEXT)

################################################################################  
class D(Thread):
    def __init__(self, twitter):
        Thread.__init__(self)
        self.twitter= twitter
        

    def p(self):
        a = datetime.now()
        
        print "CURRENT TIME ==> {0}".format(a)
        #self.twitter.home_timeline()
        sleep (6)
        
    def run(self):
        while True:
            self.p()
        

if __name__ == "__main__":
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
   
    
    twitter.start()
    
    ## d = D(twitter)
    ## d.daemon = True
    ## d.start()
    t = T_date(twitter)
    t.daemon = True
    t.start()
    while True:
        twitter.delete_replies()
        twitter.home_timeline()
        #twitter.date_status(text)
        for query in QUERYS:
            twitter.run_search(query,replays)
            sleep(70)
        sleep(randint(60,120))
        y = twitter.get_replays()
        for c in y:
            print "Tweet from @{0} ID: {1}".format(c[1].encode('utf-8'), c[0])
            print c[2].encode('utf-8'), '\n'
        
