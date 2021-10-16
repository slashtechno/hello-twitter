import tweepy
import config

print("Hello, world!")

CONSUMER_KEY = str(config.CONSUMER_KEY)
CONSUMER_SECRET = str(config.CONSUMER_SECRET)
ACCESS_KEY = str(config.ACCESS_KEY)
ACCESS_SECRET = str(config.ACCESS_SECRET)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter = tweepy.API(auth)
twitter.update_status("Hello, world!")
