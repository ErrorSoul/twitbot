#coding: utf-8

import webbrowser
from twython import Twython


CONSUMER_KEY = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET)

auth = twitter.get_authentication_tokens()
webbrowser.open(auth['auth_url'])
print auth['auth_url']
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

oauth_verifier = raw_input('What is the PIN? ') 
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
final_step = twitter.get_authorized_tokens(oauth_verifier)

print final_step 
