#coding: utf-8
import time
from twython import Twython, TwythonError
CONSUMER_KEY       = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET    = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
OAUTH_TOKEN        = "1964645443-7XZiMnTEN0fp5e2CvuyYrsM8YralkeCfya6y2Th"
OAUTH_TOKEN_SECRET = "hcA1vYDtB5e3XVFHRzunNP5VBO0JBvxDGKeAIab3w"

twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,
                  OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

g = u"жид"
while True:
    try :
        twitter.update_status(status='See how easy using Twython is!')
    except TwythonError:
        time.sleep(5)
    
## t=  twitter.search(q=g)

## for c in  t["statuses"]:
##     for d in c:
##         print d + " = " , c[d]

