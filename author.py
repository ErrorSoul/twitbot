

import webbrowser
from twython import Twython


CONSUMER_KEY = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET)

auth = twitter.get_authentication_tokens()


g =  auth['auth_url']
print g
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

oauth_verifier = int(raw_input("what is the Pin: "))
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                 OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
final_step = twitter.get_authorized_tokens(oauth_verifier)

print final_step , "ffffffffffff"
