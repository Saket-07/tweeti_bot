from bs4 import BeautifulSoup
from bing_image_downloader import downloader
from decouple import config
from datetime import *
import tweepy
import random
import requests
import time as tim
import nltk.data
import shutil


auth = tweepy.OAuthHandler(config("CONSUMER_KEY"), config("CONSUMER_SECRET"))
auth.set_access_token(config("ACCESS_KEY"), config("ACCESS_SECRET"))
api = tweepy.API(auth)

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def post_bird_tweet():
    bird_index = random.randint(1, 10973)
    bird_file = open("birds_list.txt", encoding="utf-8")

    bird = ''
    for position, line in enumerate(bird_file):
        if position == bird_index:
            bird = line
    bird_file.close()

    bird = bird.replace(' ', '_').strip()

    bird_url = "https://en.wikipedia.org/wiki/" + bird
    print(bird_url)
    response = requests.get(
        url=bird_url,
    )
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all("p")

    overview = ''
    for sentence in data:
        sentence = sentence.getText()
        if 'The ' in sentence:
            overview = tokenizer.tokenize(sentence)
            break

    overview = overview[0]

    for i in range(len(overview)):

        if i == len(overview):
            break
        if overview[i] == '[':
            overview = overview[:i] + overview[i + 3:]

    if len(overview) > 280:
        post_bird_tweet()
        return

    downloader.download(bird, limit=1, output_dir='bird_photo', adult_filter_off=True, force_replace=False,
                        timeout=60, verbose=True)

    bird_image = 'bird_photo\\' + bird + '\\image_1.jpg'
    api.update_with_media(bird_image, overview)


    dir = "bird_photo"

    shutil.rmtree(dir)


bird_posting_time = datetime.now()+timedelta(seconds=20)

while True:
    while datetime.now() < bird_posting_time:
        tim.sleep(1)
    post_bird_tweet()
    bird_posting_time += timedelta(hours=12)
