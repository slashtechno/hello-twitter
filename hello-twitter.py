from http import client
import os
import tweepy
import time
import json
import requests
from webbrowser import open as open_url
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
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


id_file = "id.txt"

# authenticate with Twitter
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
)
print(oauth2_user_handler.get_authorization_url())
open_url(oauth2_user_handler.get_authorization_url())
access_token = oauth2_user_handler.fetch_token(
    # REDIRECT_URI + "?state=state&code=" + input("Authorization code: ")
    input("Authorization URL: ")
)
print(access_token)
print("\n")
client = tweepy.Client(access_token)


while True:
    # go through new mentions and scan them for a tag
    last_scanned_id = retrieve_id(id_file)
    mentions = client.mentions_timeline(tweet_mode="extended", count=200)
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
                        client.update_status("@"+mention.user.screen_name
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
                        client.update_status("@"+mention.user.screen_name + " Team Seas has removed " + str(stats["count"])
                                          + " pounds of trash from the world's oceans!", in_reply_to_status_id=mention.id)
                    except tweepy.errors.Forbidden:
                        pass
                    print("Replied to @" + mention.user.screen_name)
                    target_content = "True"
                else:
                    target_content = "False"

    print("last scanned ID was " + str(last_scanned_id))
    # Only scan mentions after last scanned mention
    mentions = client.mentions_timeline(
        since_id=last_scanned_id, tweet_mode="extended", count=200)
    for mention in reversed(mentions):
        # Reply to tweets with specified tag/text
        if "#HelloWorld" in mention.full_text:
            print("ID for the mention above: "+str(mention.id))
            print(mention.full_text)  # print the mention's text
            last_scanned_id = mention.id
            write_last_id(last_scanned_id, id_file)
            try:
                client.update_status("@"+mention.user.screen_name+" Hi",
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
                client.update_status("@"+mention.user.screen_name+" Team Seas has removed " + str(stats["count"]) + " pounds of trash from the world's oceans!",
                                  in_reply_to_status_id=mention.id)
            except tweepy.errors.Forbidden:
                pass
            print("Replied to @" + mention.user.screen_name)
    time.sleep(21)  # To avoid rate limiting
