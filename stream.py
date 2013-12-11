from twython import Twython
from twython import TwythonStreamer

CONSUMER_KEY = "Dc8GNbgcOklJie3TV2V0A"
CONSUMER_SECRET = "QducleApTwunlqZmNM0AdhwlhWpoDJ44agk6UnPs"
oauth_token_secret = '1uZiuWCXwE78og5SHGhz85opeAIqoyskNPT3OeHftlfnO'
oauth_token='74446564-IasJQxyO7JzgnbRhyl5bamFQSzUwQDG4LB68KHjqZ'


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
       
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code
stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret)
#print stream.statuses.firehose()

stream.user(replies=all)

