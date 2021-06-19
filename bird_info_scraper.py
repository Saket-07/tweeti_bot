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

    bird = bird.strip()
    print(bird)
    bird_with_ = bird.replace(' ', '_')

    bird_url = "https://en.wikipedia.org/wiki/" + bird_with_
    print(bird_url)
    response = requests.get(
        url=bird_url,
    )
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all("p")

    overview = ''
    for sentence in data:
        sentence = sentence.getText()
        if 'The ' in sentence or bird in sentence:
            overview = tokenizer.tokenize(sentence)
            break

    try:
        overview = overview[0]
    except:
        print("Something wrong with getting overview")
        post_bird_tweet()
        return

    for i in range(len(overview)):

        if i == len(overview):
            break
        if overview[i] == '[':
            overview = overview[:i] + overview[i + 3:]

    if len(overview) > 280:
        post_bird_tweet()
        return

    search_bird = bird_with_ + ' bird'
    downloader.download(search_bird, limit=1, output_dir='bird_photo', adult_filter_off=True, force_replace=False,
                        timeout=60, verbose=True)

    bird_image_1 = 'bird_photo/' + bird_with_.strip() + '/Image_1.jpg'
    bird_image_2 = 'bird_photo/' + bird_with_.strip() + '/Image_1.jpeg'
    bird_image_3 = 'bird_photo/' + bird_with_.strip() + '/Image_1.png'

    try:
        api.update_with_media(bird_image_1, overview)
    except tweepy.error.TweepError:
        try:
            api.update_with_media(bird_image_2, overview)
        except tweepy.error.TweepError:
            try:
                api.update_with_media(bird_image_3, overview)
            except tweepy.error.TweepError:
                print('Image not downloaded')
                post_bird_tweet()
                return
    shutil.rmtree('bird_photo')


while True:
    post_bird_tweet()
    tim.sleep(43200)
