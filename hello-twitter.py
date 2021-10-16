import tweepy
import config
# PYTHONDONTWRITEBYTECODE = 0
print("Hello, world!\n")

CONSUMER_KEY = str(config.CONSUMER_KEY)
CONSUMER_SECRET = str(config.CONSUMER_SECRET)
ACCESS_KEY = str(config.ACCESS_KEY)
ACCESS_SECRET = str(config.ACCESS_SECRET)

# authenticate with Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# create api object to interact with Twitter
api = tweepy.API(auth)
mentions = api.mentions_timeline()
# go through mentions and scan them for a tag
for mention in mentions:
    print(mention.text)  # print the mention's text
    print("ID for the mention above: "+str(mention.id))
