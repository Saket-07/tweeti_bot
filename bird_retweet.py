from decouple import config
import tweepy
import time as tim
from datetime import *


auth = tweepy.OAuthHandler(config("CONSUMER_KEY"), config("CONSUMER_SECRET"))
auth.set_access_token(config("ACCESS_KEY"), config("ACCESS_SECRET"))
api = tweepy.API(auth)

def cmp(ab):
    return ab.created_at

def retweet():
    search_results = api.search(q="#bird #birds", count=100, lang="en")
    search_results+=(api.search(q="#birdphotography", count=100, lang="en"))
    search_results.sort(reverse=True, key=cmp)

    api.retweet(search_results[0].id)

bird_retweet_time = datetime.now()
while True:
    while datetime.now() < bird_retweet_time:
        tim.sleep(1)
    retweet()
    bird_retweet_time += timedelta(hours=4)

