import tweepy
import config
# PYTHONDONTWRITEBYTECODE = 0

CONSUMER_KEY = str(config.CONSUMER_KEY)
CONSUMER_SECRET = str(config.CONSUMER_SECRET)
ACCESS_KEY = str(config.ACCESS_KEY)
ACCESS_SECRET = str(config.ACCESS_SECRET)

id_file = "id.txt"


def retrieve_id(file):
    IDs_read = open(file, "r")
    last_id = IDs_read.read().strip()
    # print("Last ID was " + str(last_id))
    IDs_read.close()
    return last_id


def write_last_id(id, file):
    IDs_write = open(file, "w")
    IDs_write.write(str(id))
    IDs_write.close()
    return


# authenticate with Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# create api object to interact with Twitter
api = tweepy.API(auth)

# go through mentions and scan them for a tag ignoring mentions already scanned
last_scanned_id = retrieve_id(id_file)
# Only scan mentions after last scanned mention
mentions = api.mentions_timeline(
    since_id=last_scanned_id, tweet_mode="extended")
for mention in reversed(mentions):
    print(mention.full_text)  # print the mention's text
    print("ID for the mention above: "+str(mention.id))
    # Reply to tweets with specified tag/text
    if "#HelloWorld" in mention.full_text:
        last_scanned_id = mention.id
        write_last_id(last_scanned_id, id_file)
        api.update_status("@"+mention.user.screen_name+" Hi",
                          in_reply_to_status_id=mention.id)
        print("Replied to @" + mention.user.screen_name)
