from decouple import config
import tweepy
import time
import random
import requests
import nltk.data
import shutil
import wikipedia
from bing_image_downloader import downloader
from bs4 import BeautifulSoup

auth = tweepy.OAuthHandler(config("CONSUMER_KEY"), config("CONSUMER_SECRET"))
auth.set_access_token(config("ACCESS_KEY"), config("ACCESS_SECRET"))
api = tweepy.API(auth)

weather_api_key = config("WEATHER_API_KEY")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sup_salutations = ['sup', 'whats up', "what's up", 'wassup']
sup_replies = [' Hey Yourself! Nothing much, I just got myself some bird food \U0001f600',
               ' Ceiling! Please excuse me for my poor sense of humour.',
               ' Hey There! Nothing much, same old.',
               ' Same old, same old.',
               ' Hi! Tough day at work today :(',
               ' Nothing, just tired from a long flight.']

hi_salutations = ['hi', 'hello', 'hola']
hi_replies = [' Hey Yourself!',
              ' Hey you :)',
              ' Hey ya!!!',
              ' Hi there \U0001f600',
              ' Hola amigo!!']


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


def check_if_bird(url):
    response = requests.get(
        url=url,
    )
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all("a")
    for a in data:
        try:
            if "Aves" in a.getText():
                return True
        except KeyError:
            pass
    return False


def tweet_bird_info(bird_name, mention):
    overview = ''
    url = ''
    try:
        overview = wikipedia.summary(bird_name, auto_suggest=False, sentences=1)
        url = wikipedia.page(bird_name, auto_suggest=False).url
    except wikipedia.DisambiguationError as e:
        s = e.options
        bird_file = open("birds_list.txt", encoding="utf-8")
        readfile = bird_file.read()
        flag = 1
        for name in s:
            if name in readfile:
                bird_name = name
                flag = 0
                break
        if flag:
            api.update_status('@' + mention.user.screen_name + " Sorry, I haven't heard of this bird \U0001F615",
                              mention.id)
            return
        url = wikipedia.page(bird_name, auto_suggest=False).url
        overview = wikipedia.summary(bird_name, auto_suggest=False)
    except wikipedia.PageError as e:
        api.update_status('@' + mention.user.screen_name + " Sorry, I can't find the bird you searched for.",
                          mention.id)
        return

    if not check_if_bird(url):
        api.update_status('@' + mention.user.screen_name + " Sorry, I haven't heard of this bird \U0001F615",
                          mention.id)
        return

    if len(overview) > 250:
        api.update_status(
            '@' + mention.user.screen_name + " " + "The info about the bird is too large, please refer this url: " + url,
            mention.id)
        return

    downloader.download(bird_name.strip(), limit=1, output_dir='bird_photo', adult_filter_off=True, force_replace=False,
                        timeout=60, verbose=True)

    bird_image_1 = 'bird_photo/' + bird_name.strip() + '/Image_1.jpg'
    bird_image_2 = 'bird_photo/' + bird_name.strip() + '/Image_1.jpeg'
    bird_image_3 = 'bird_photo/' + bird_name.strip() + '/Image_1.png'
    try:
        api.update_with_media(bird_image_1, '@' + mention.user.screen_name + ' ' + overview)
    except tweepy.error.TweepError:
        try:
            api.update_with_media(bird_image_2, '@' + mention.user.screen_name + ' ' + overview)
        except tweepy.error.TweepError:
            try:
                api.update_with_media(bird_image_3, '@' + mention.user.screen_name + ' ' + overview)
            except tweepy.error.TweepError:
                print('Image not downloaded')
                api.update_status('@' + mention.user.screen_name + " " + overview, mention.id)
                return
    shutil.rmtree('bird_photo')
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
        salu_flag = 0

        if 'unfollow me' in mention.full_text.lower() and salu_flag == 0:
            print('Found unfollow me request, unfollowing user...', flush=True)
            api.destroy_friendship(mention.user.screen_name)
            api.update_status('@' + mention.user.screen_name + ' As you say \U0001F97A', mention.id)
            salu_flag = 1

        if 'follow me' in mention.full_text.lower() and salu_flag == 0:
            print('Found follow me request, following user...', flush=True)
            api.create_friendship(mention.user.screen_name)
            api.update_status('@' + mention.user.screen_name + ' Done!', mention.id)
            salu_flag = 1

        if 'joke' in mention.full_text.lower() and salu_flag == 0:
            jokes_url = "https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun,Christmas?blacklistFlags=religious,political,racist,sexist,explicit&format=txt"
            response = requests.get(jokes_url)

            api.update_status('@' + mention.user.screen_name + " " + response.text, mention.id)
            print("joke request found, replying....", flush=True)
            salu_flag = 1

        if 'bird info' in mention.full_text.lower() and salu_flag == 0:
            print('found bird info request, replying...', flush=True)
            # extracting bird name
            words = mention.full_text.lower().split()
            # print(words)
            itemp = 3
            temp_bird_name = ''
            while itemp < len(words):
                temp_bird_name += words[itemp] + ' '
                itemp += 1
            # temp_bird_name += 'bird'
            # if 'bird' not in temp_bird_name:
            #    temp_bird_name += 'bird'
            temp_bird_name.strip()
            print("The bird name extracted is: ", temp_bird_name)
            tweet_bird_info(temp_bird_name, mention)
            salu_flag = 1

        if 'movie' in mention.full_text.lower() and salu_flag == 0:
            movie_url = "https://www.imdb.com/list/ls063596142/"
            print(movie_url)
            response = requests.get(
                url=movie_url,
            )
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.find_all("img")
            movie_list = list()
            for image in data:
                if image['alt'].strip() != 'loading' and image['alt'].strip() != 'list image':
                    movie_list.append(image['alt'].strip())

            movie_indices = random.sample(range(0, 99), 3)

            print("found movie request, suggesting movies...")
            api.update_status('@' + mention.user.screen_name + " " +
                              "Here are some movie recommendations for ya:" +
                              "\n1. " + movie_list[movie_indices[0]] +
                              "\n2. " + movie_list[movie_indices[1]] +
                              "\n3. " + movie_list[movie_indices[2]] +
                              "\nEnjoy :)", mention.id)
            salu_flag = 1

        if 'book' in mention.full_text.lower() and salu_flag == 0:
            book_url = "https://www.google.com/search?q=book+recommendations&rlz=1C1CHBF_enIN863IN863&oq=book+recomme&aqs=chrome.0.0i433j69i57j0l8.3592j0j7&sourceid=chrome&ie=UTF-8"
            print(book_url)
            response = requests.get(
                url=book_url,
            )
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")

            book_list = list()
            for a in data:

                try:
                    if '...' not in a.getText():
                        book_list.append(a.getText())
                except KeyError:
                    pass

            book_indices = random.sample(range(0, 15), 3)

            print("found book request, suggesting books...")
            api.update_status('@' + mention.user.screen_name + " " +
                              "Here are some nice books to read:" +
                              "\n1. " + book_list[book_indices[0]] +
                              "\n2. " + book_list[book_indices[1]] +
                              "\n3. " + book_list[book_indices[2]] +
                              "\nCheers :)", mention.id)
            salu_flag = 1

        if 'weather' in mention.full_text.lower() and salu_flag == 0:
            print('found weather request, replying...', flush=True)
            # extracting city name
            words = mention.full_text.split()
            itemp = 1
            temp_city_name = ''
            while words[itemp].lower() != 'weather':
                temp_city_name = temp_city_name + words[itemp] + ' '
                itemp += 1
            city_name = temp_city_name.strip()
            # city_name = temp_city_name[:len(temp_city_name)-1]
            weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name.lower().replace(' ',
                                                                                                           '%20') + '&appid=' + weather_api_key
            weather_response = requests.get(weather_url)
            wea_json = weather_response.json()

            if wea_json["cod"] != "404":
                current_temperature = round(wea_json["main"]["temp"] - 273.15, 1)
                current_humidity = wea_json["main"]["humidity"]
                weather_description = wea_json["weather"][0]["description"]
                api.update_status('@' + mention.user.screen_name + ' Weather forecast in ' + city_name + ':'
                                                                                                         '\n' + str(
                    weather_description) +
                                  '\nTemperature = ' + str(current_temperature) + '\u00b0 C' +
                                  '\nHumidity = ' + str(current_humidity) + '%', mention.id)
            else:
                api.update_status('@' + mention.user.screen_name + ' City not found \U0001F615', mention.id)
            salu_flag = 1

        if salu_flag == 0:
            for word in sup_salutations:
                if word in mention.full_text.lower():
                    print('found some salutations', flush=True)
                    print('responding back...', flush=True)
                    reply_index = random.randint(0, len(sup_replies) - 1)
                    api.update_status('@' + mention.user.screen_name + sup_replies[reply_index], mention.id)
                    salu_flag = 1
                    break

        if salu_flag == 0:
            for word in hi_salutations:
                if word in mention.full_text.lower():
                    print('found some salutations', flush=True)
                    print('responding back...', flush=True)
                    reply_index = random.randint(0, len(hi_replies) - 1)
                    api.update_status('@' + mention.user.screen_name + hi_replies[reply_index], mention.id)
                    salu_flag = 1
                    break

        if salu_flag ==0:
            api.update_status('@' + mention.user.screen_name + " Unfortunately I cannot recognise this command \U0001F614. Refer to the pinned tweet and try again", mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)
