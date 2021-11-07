import tweepy
import config
import time
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

while True:
    # go through new mentions and scan them for a tag
    last_scanned_id = retrieve_id(id_file)
    mentions = api.mentions_timeline(tweet_mode="extended")
    if not last_scanned_id:  # Check if there is a stored # ID
        for mention in reversed(mentions):
            # Reply to tweets with specified tag/text
            target_content = "False"
            while target_content == "False":
                if "#HelloWorld" in mention.full_text:
                    print("ID for the mention above: "+str(mention.id))
                    print(mention.full_text)  # print the mention's text
                    last_scanned_id = mention.id
                    write_last_id(last_scanned_id, id_file)
                    try:
                        api.update_status("@"+mention.user.screen_name
                                          + " Hi", in_reply_to_status_id=mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            pass
                        else:
                            raise error
                    print("Replied to @" + mention.user.screen_name)
                    target_content = "True"
                else:
                    target_content = "False"

    print("last scanned ID was " + str(last_scanned_id))
    # Only scan mentions after last scanned mention
    mentions = api.mentions_timeline(
        since_id=last_scanned_id, tweet_mode="extended")
    for mention in reversed(mentions):
        # Reply to tweets with specified tag/text
        if "#HelloWorld" in mention.full_text:
            print("ID for the mention above: "+str(mention.id))
            print(mention.full_text)  # print the mention's text
            last_scanned_id = mention.id
            write_last_id(last_scanned_id, id_file)
            try:
                api.update_status("@"+mention.user.screen_name+" Hi",
                                  in_reply_to_status_id=mention.id)
            except tweepy.TweepError as error:
                if error.api_code == 187:
                    pass
                else:
                    raise error
            print("Replied to @" + mention.user.screen_name)
    time.sleep(12)  # To avoid rate limiting
