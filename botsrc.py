from decouple import config
import tweepy
import time
import random

auth = tweepy.OAuthHandler(config("CONSUMER_KEY"), config("CONSUMER_SECRET"))
auth.set_access_token(config("ACCESS_KEY"), config("ACCESS_SECRET"))
api = tweepy.API(auth)


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    last_seen_id = retrieve_last_seen_id('last_seen_id.txt')
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, 'last_seen_id.txt')
        sup_salutations = ['sup', 'whats up', "what's up", 'wassup']
        sup_replies = [' Hey Yourself! Nothing much, I just got myself some bird food.',
                       ' Ceiling! Please excuse me for my poor sense of humour.', ' Hey There! Nothing much, same old.',
                       ' Same old, same old.', ' Hi! Tough day at work today :(',
                       ' Nothing, just tired from a long flight.']
        for word in sup_salutations:
            if word in mention.full_text.lower():
                print('found some salutations', flush=True)
                print('responding back...', flush=True)
                reply_index = random.randint(0, 5)
                api.update_status('@' + mention.user.screen_name +
                                  sup_replies[reply_index], mention.id)
                break


while True:
    reply_to_tweets()
    time.sleep(15)
