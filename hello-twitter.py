import os
import tweepy
import time
import json
import requests
from dotenv import load_dotenv

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

# PYTHONDONTWRITEBYTECODE = 0

load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")


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
    mentions = api.mentions_timeline(tweet_mode="extended", count=200)
    if not last_scanned_id:  # Check if there is a stored # ID
        for mention in mentions:
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
                    except tweepy.errors.Forbidden:
                        pass
                    print("Replied to @" + mention.user.screen_name)
                    target_content = "True"

                elif "\#TeamSeas" in mention.full_text:
                    print("ID for the mention above: "+str(mention.id))
                    print(mention.full_text)  # print the mention's text
                    last_scanned_id = mention.id
                    write_last_id(last_scanned_id, id_file)
                    try:
                        stats = json.loads(requests.get(
                            "https://tscache.com/donation_total.json").text)
                        print(stats["count"])
                        api.update_status("@"+mention.user.screen_name + " Team Seas has removed " + str(stats["count"])
                                          + " pounds of trash from the world's oceans!", in_reply_to_status_id=mention.id)
                    except tweepy.errors.Forbidden:
                        pass
                    print("Replied to @" + mention.user.screen_name)
                    target_content = "True"
                else:
                    target_content = "False"

    print("last scanned ID was " + str(last_scanned_id))
    # Only scan mentions after last scanned mention
    mentions = api.mentions_timeline(
        since_id=last_scanned_id, tweet_mode="extended", count=200)
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
            except tweepy.errors.Forbidden:
                pass
            print("Replied to @" + mention.user.screen_name)
        if "#TeamSeas" in mention.full_text:
            print("ID for the mention above: "+str(mention.id))
            print(mention.full_text)  # print the mention's text
            last_scanned_id = mention.id
            write_last_id(last_scanned_id, id_file)
            try:
                stats = json.loads(requests.get(
                    "https://tscache.com/donation_total.json").text)
                print(stats["count"])
                api.update_status("@"+mention.user.screen_name+" Team Seas has removed " + str(stats["count"]) + " pounds of trash from the world's oceans!",
                                  in_reply_to_status_id=mention.id)
            except tweepy.errors.Forbidden:
                pass
            print("Replied to @" + mention.user.screen_name)
    time.sleep(21)  # To avoid rate limiting
