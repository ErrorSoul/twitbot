
#coding: utf-8 

from twython import Twython, TwythonError 
from random import choice, randint, shuffle  
from datetime import datetime
from threading import Thread
from time import  time, sleep
from text import replays, night, afternoon, morning
from decorators import wrapper

CONSUMER_KEY       = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET    = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
OAUTH_TOKEN        = "1964645443-mmEaq9TWNGoXoZ9glFrE96Yx9ktHHkCRUxCFfms"
OAUTH_TOKEN_SECRET = "2PbSnYpJdGJdv1TF1F3eCF5SRdigCcwVYRpvsrfELta0t"
QUERYS = [u"хахол", u"хохол"]
TEXT = [morning, afternoon, night]
## map(shuffle,TEXT)
## for c in range(3):
##     shuffle(replays)

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
        self.time = [(4, 55), (17, 55), (19, 55)]

        #count of replies of day
        self.replies_limit = 0
        self.replies_count = 35
        self.flag = True

        #users victims
        self.users = (u"feeling_so_real", u"captein_treniki",
                      u"fe_city_boy", u"drunktwi",
                      u"Doppler_Effectt", u"koffboy")
        
    
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
            print "last user", users[-1]
            print "#" * 40,'\n'
        return users

################################## RUN SEARCH ############################################        

    def run_search(self, query, text):
        self.query = query
        result =  self.twitter.search(q=query)
        if result:
            users = self.get_users(result)
            for user in users:
                    if self.replies_count < self.replies_limit:
                        self.update_status(text,user)
                    else:
                        break
                    
            sleep(randint(180,210))
        else:
            sleep(randint(240, 480))
            
    def update_status(self, text, user):
        q_id = self.id if self.query == u"хохол" else self.jd
        #replayed tweet or not 
        if  user[0] > q_id[0]:
            
                self.twitter.update_status(status= u"@{0} {1}".format(
                                           user[1], choice(text)),
                                           in_reply_to_status_id=user[0])
                self.replies_count +=1
                #save last tweet id 
                q_id[0] = user[0]
                sleep(randint(400,560))

    @wrapper(n=40)
    def big_search(self):
        for query in QUERYS:
            self.run_search(query, replays)
            sleep(70)
        sleep(randint(60,120))
        
            

################################################################################
    

   
################################ HOME TIMELINE ######################################
    @wrapper()
    def home_timeline(self):
        """ update count of replies
            update timeline(random rt or fav in homeline)
        """
        hour = self.data.hour
        
        #debug
        print self.replies_count, "count"
        print self.replies_limit, "limit"
        #end debug

        def update_replies_count():
            """update flags and replies limit"""
            if self.flag:
                if hour in (10,17):
                    self.replies_limit = randint(3,12)
                    self.flag = False
                    self.replies_count = 0

        def timeline_updates():
            """check time and run if time rt and fav in homeline"""
            if (hour in range(0, 3) or hour in range(9, 24)):
                print "CHECK TIMELINE UPDATES"
                result = self.get_home_timeline(count=30,exclude_replies=1,
                                            since_id=self.t_id)
                if result:
                    tw = [tweet["id"] for tweet in result if (tweet['user']['screen_name'] != u"ghohol" and
                                                            not tweet['entities']['user_mentions'])]
                    if tw:
                        self.t_id = tw[0]
                        rt_or_fav = lambda func : map(func, filter(lambda x:x % 127 == 0, tw))
                        if (randint(0,7) == randint(0,7)):                           
                            map(rt_or_fav,(self.retweet, self.create_favorite))
            else:
                print "NO TIMELINE UPDATES" 
                            
        
        #update_replies_count()
        timeline_updates()                

                    
         
       

################################### Tools #############################################
    for name in ("retweet", "create_favorite", "destroy_status",
                 "destroy_friendship"):
        exec("""def {0}(self, id):
                    self.twitter.{0}(id=id)""".format(name))

    for name in ("get_home_timeline", "get_direct_messages", "get_friends_ids",
                 "get_followers_ids", "get_user_timeline", "show_status",
                 "update_status"):

        exec("""def {0}(self, *args, **kwargs):
                    return self.twitter.{0}(*args, **kwargs)""".format(name))
    
    @property
    def data(self):
        return datetime.now()

      
    def my_reetwets(self):
        """return id of my retweets"""
        retweets =  self.twitter.retweeted_of_me()
        retweets_id = [c["id"] for c in retweets]
        return retweets_id

    @wrapper(n=30)
    def tw_reader(self, tw):
        for c in tw:
            print "Tweet from @{0} ID: {1}".format(c[1].encode('utf-8'), c[0])
            print c[2].encode('utf-8'), '\n'

    
             
       
       

############################### GET REPLAYS #############################################
    @wrapper(n=0)
    def get_replays(self):
        dirty_list = (u"хуй", u"пидор",u"пидар", u"пидр",
                      u"бля", u"блядь", u"сука",u"ебень",
                      u"гондон", u"гандон", u"шлюха",
                      u"чмо", u"залупа", u"eблан",
                      u"козел", u"казел", u"козлина",
                      u"тварь", u"долбоеб", u"бандеровец",
                      u"блять", u"уеби", u"бендеровец",
                      u"дебил", u"дибил", u"петух",
                      u"питух", u"петушок", u"ебали",
                      u"хуя"
                      )
        
        

        def is_shit(tweet):
            t = tweet[2].lower()
            for word in dirty_list:
                if word in t:
                    return word
            return False
        
    
        repl = self.twitter.get_mentions_timeline(include_rts = 0,
                                                  since_id = self.m_id)
        print repl, "repl"

        if repl:
            print "IF REPL"
            repl =[(c["id"],c["user"]["screen_name"],c["text"]) for c
                   in repl if u"RT" not in c["text"]]
            self.m_id = repl[0][0]
            repl = filter(is_shit, repl)
            if repl:
                print "IF REPL INNER"
                print "Try send mention for dirty reply"
                for tw in repl:
                    (self.retweet(tw[0]) if randint(0,1)
                    else self.update_dirty_status(tw[1],tw[0]))
                   
            #return repl
        print repl, "repl"
        return repl 
        
            
    def update_dirty_status(self, name, id):
        answers = [ u"Ты еще и ругаешься",
                    u"Попросил бы без оскорблений",
                    u"Очень грубо",
                    u"А можно без мата?",
                    u"Кто так обзывается, сам так называется",
                    u"Сколько мата тьфу ты, бля"
                  ] 
              

        self.update_status(status= u"@{0} {1}".format(
                                   name, choice(answers)),
                                   in_reply_to_status_id=id)
        sleep(randint(140,280))

    
######################################## STEAL TWEET ################################
    @wrapper()
    def steal_tweets(self, d):
        hour = d.hour
        print hour, "FGGGGGGGGGGGGGGGGJJGJGJGJGJJJJJJJJJJJJJJJJJ"
        if hour in (5, 16):
            print "TIME TO STEAL TWEETS"
            #get my tweets
            my_tweets = self.twitter.get_user_timeline(count=200, exclude_replies=1)
            my_tweets = [c["text"] for c in my_tweets]
            #get victim's tweets
            get_victims_timeline = self.get_victims_timeline(my_tweets)
            victims_tweets = map(get_victims_timeline, self.users)
            for tweet in victims_tweets:
                print tweet
                if tweet is not None:
                    self.twitter.update_status(status=tweet)
                    sleep(3600)
            print "STEALING TWEETS IS OVER"
        else:
            sleep(3600)
       
        
        
    def get_victims_timeline(self, text):
        def victims_tweets(name):
            raw_tweets =  self.twitter.get_user_timeline(screen_name=name, exclude_replies=1, count=60)
            print "dddd"
            print "raw_tweets", len(raw_tweets)
            tweets = raw_tweets[-1:len(raw_tweets):-1]
            tweets = [c for c in tweets if (not c["entities"]['urls'] and
                                                  len(c['entities'])==4 and
                                                  not c['entities']['user_mentions']
                                                  )]

            sample_tweet = [c['text'] for c in tweets if c['text'] not in text]
            if sample_tweet:
                sample_tweet = sample_tweet[-1]
                print sample_tweet.encode('utf-8')
                return sample_tweet
            else:
                return None
        return victims_tweets
            

######################################## START ########################################
    @wrapper(n=0)
    def start(self):
        def complete(attr):
            d = {"self.jd":self.jd, "self.id":self.id,
                 "self.t_id":self.t_id, "self.m_id":self.m_id}
            print "##### COMPLETE #####\n"
            print "{0} = {1} {2} complete\n".format(attr, d[attr],'.' * 25)

        while ((not self.m_id or not self.t_id) or
               (self.id[0] == 0 or self.jd[0] == 0)):
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

###################################### DELETE REPLIES  ##############################################                    

    @wrapper()
    def delete_replies(self):
        if self.data.hour == 23:
            print "START CLEAR TWEETS"
            tweets = self.get_user_timeline(count=100)
            tweets = (c["id"] for c in tweets if c["in_reply_to_user_id"] )
            sleep(15)
            map(self.destroy_status, tweets)
        else:
            print "NO CLEAN"


 
################################## UNFOLLOW ######################################
    @wrapper()
    def unfollow_who_not_follow_back(self):
        data = self.data
        #clean followers every odd day
        if data.day % 2 == 0 and data.hour == 1:
            # "stars" id's
            stars_id = (462792965, 14774424, 344512640,
                        265008715, 412493190, 254655960,
                        179484444, 90647948, 408437933,
                        98422492,  81297044,  250801581)
            print "UNFOLLOWING START"           
            #get friends id's
            friends_ids = self.get_friends_ids()[u"ids"]
            friends_ids = (id for id in friends_ids if id not in stars_id)
            #get followers ids
            followers_ids = self.twitter.get_followers_ids()[u"ids"]
            #unfollowing list
            destroy_list = (user_id for user_id in friends_ids 
                            if user_id not in followers_ids)
            map(self.twitter.destroy_friendship, destroy_list)
            print "UNFOLLOWING END"
            
                    
                
############################### DATE STATUS ############################################

    def date_status(self, text):
       
        
        current_time = self.data
        print "current time = {0}".format(str(current_time))
        #this part for count_replies
        if current_time.hour in (9, 16):
            self.flag = True
            sleep(randint(1600, 2400))
        
        ## def part_of_day(time_of_day):
        ##     """return True if current time equal time_of_day"""
        ##     return (current_time.hour == time_of_day[0] and
        ##             current_time.minute in range(time_of_day[1]))

        ## check_time = filter(part_of_day, self.time)
        ## if check_time:
        ##     print "check_time"
        ##     message = choice(text[self.time.index(check_time[0])])
        ##     try:
        ##         self.twitter.update_status(status= u"{0}".format(message))
        ##         sleep(randint(1600, 2400))
        ##     except TwythonError as err:
        ##         print err
        ##         sleep(480)
        else:
            sleep(randint (1200, 1800))

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
        self.twitter.steal_tweets(a)
        
        
    def run(self):
        while True:
            self.p()
        
def main():
    #connection and login 
    twitter = TwitBot(CONSUMER_KEY,CONSUMER_SECRET,
                      OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    #start twiter
    twitter.start()
    #init thread
    d = D(twitter)
    d.daemon = True
    d.start()
    #init thread
    t = T_date(twitter)
    t.daemon = True
    t.start()
    while True:
        twitter.unfollow_who_not_follow_back()
        twitter.delete_replies()
        twitter.home_timeline()
        repls = twitter.get_replays()
        twitter.tw_reader(repls)
    
if __name__ == "__main__":
    main()
    
     
         
    

