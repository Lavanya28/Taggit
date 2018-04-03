'''
    #TAGGIT: SOCIAL-SENSING FOR SENTIMENT ANALYSIS, TOPIC MODELING AND FAKE NEWS DETECTION
    File responsible to fetch all our data

    for today: sentiment analysis, LDA (scikit-learn)
'''

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import tweepy
from credentials import consumer_key, consumer_secret, access_token_secret, access_token

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('data.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#trump', '#election', '#hillary'])
