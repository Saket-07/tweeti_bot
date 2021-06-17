from decouple import config
import tweepy
import time
import random
import requests

auth = tweepy.OAuthHandler(config("CONSUMER_KEY"), config("CONSUMER_SECRET"))
auth.set_access_token(config("ACCESS_KEY"), config("ACCESS_SECRET"))
api = tweepy.API(auth)

weather_api_key = config("WEATHER_API_KEY")


def retrieve_last_replied_dmid(file_name):
    f_read = open(file_name, 'r')
    last_replied_dmid = int(f_read.read().strip())
    f_read.close()
    return last_replied_dmid


def store_last_replied_dmid(last_replied_dmid, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_replied_dmid))
    f_write.close()
    return


def reply_dms():
    last_replied_dmid = retrieve_last_replied_dmid('last_replied_dm.txt')
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    dir_messages = api.list_direct_messages()

    sup_salutations = ['sup', 'whats up', "what's up", 'wassup']
    sup_replies = ['Hey Yourself! Nothing much, I just got myself some bird food \U0001f600',
                   'Ceiling! Please excuse me for my poor sense of humour.',
                   'Hey There! Nothing much, same old.',
                   'Same old, same old.',
                   'Hi! Tough day at work today :(',
                   'Nothing, just tired from a long flight.']

    hi_salutations = ['hi', 'hello', 'hola']
    hi_replies = ['Hey Yourself!',
                  'Hey you :)',
                  'Hey ya!!!',
                  'Hi there \U0001f600',
                  'Hola amigo!!']

    for dir_message in dir_messages:
        if dir_message.id == str(last_replied_dmid):
            break

        print(str(dir_message.id) + ' - ' + str(dir_message.message_create['sender_id']) + ' - ' +
              dir_message.message_create["message_data"]["text"], flush=True)

        if dir_message.message_create['sender_id'].strip() != '1357654871948865536':
            salu_flag = 0
            if 'unfollow me' in dir_message.message_create["message_data"]["text"].lower() and salu_flag == 0:
                print('Found unfollow me request, unfollowing user...', flush=True)
                api.destroy_friendship(dir_message.message_create['sender_id'])
                api.send_direct_message(dir_message.message_create['sender_id'], 'As you say \U0001F97A')
                salu_flag = 1

            if 'follow me' in dir_message.message_create["message_data"]["text"].lower() and salu_flag == 0:
                print('Found follow me request, following user...', flush=True)
                api.create_friendship(dir_message.message_create['sender_id'])
                api.send_direct_message(dir_message.message_create['sender_id'], 'Done!')
                salu_flag = 1

            if 'joke' in dir_message.message_create["message_data"]["text"].lower() and salu_flag == 0:
                jokes_url = "https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun,Christmas?blacklistFlags=religious,political,racist,sexist,explicit&format=txt"
                response = requests.get(jokes_url)
                api.send_direct_message(dir_message.message_create['sender_id'], response.text)
                print("joke request found, replying....", flush=True)
                salu_flag = 1

            if 'weather' in dir_message.message_create["message_data"]["text"].lower() and salu_flag == 0:
                print('found weather request, replying...', flush=True)
                # extracting city name
                words = dir_message.message_create["message_data"]["text"].split()
                itemp = 0
                temp_city_name = ''
                while words[itemp].lower() != 'weather':
                    temp_city_name = temp_city_name + words[itemp] + ' '
                    itemp += 1
                city_name = temp_city_name.strip()
                # city_name = temp_city_name[:len(temp_city_name)-1]
                weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name.lower().replace(' ',
                                                                                                               '%20') + \
                              '&appid=' + weather_api_key
                weather_response = requests.get(weather_url)
                wea_json = weather_response.json()

                if wea_json["cod"] != "404":
                    current_temperature = round(wea_json["main"]["temp"] - 273.15, 1)
                    current_humidity = wea_json["main"]["humidity"]
                    weather_description = wea_json["weather"][0]["description"]
                    api.send_direct_message(dir_message.message_create['sender_id'],
                                            'Weather forecast in ' + city_name + ':'
                                                                                 '\n' + str(weather_description) +
                                            '\nTemperature = ' + str(current_temperature) + '\u00b0 C' +
                                            '\nHumidity = ' + str(current_humidity) + '%')
                else:
                    api.send_direct_message(dir_message.message_create['sender_id'], 'City not found \U0001F615')
                salu_flag = 1

            if salu_flag == 0:
                for word in sup_salutations:
                    if word in dir_message.message_create["message_data"]["text"].lower():
                        print('found some salutations', flush=True)
                        print('responding back...', flush=True)
                        reply_index = random.randint(0, len(sup_replies) - 1)
                        api.send_direct_message(dir_message.message_create['sender_id'], sup_replies[reply_index])
                        salu_flag = 1
                        break

            if salu_flag == 0:
                for word in hi_salutations:
                    if word in dir_message.message_create["message_data"]["text"].lower():
                        print('found some salutations', flush=True)
                        print('responding back...', flush=True)
                        reply_index = random.randint(0, len(hi_replies) - 1)
                        api.send_direct_message(dir_message.message_create['sender_id'], hi_replies[reply_index])
                        salu_flag = 1
                        break
    last_replied_dmid = dir_messages[0].id
    store_last_replied_dmid(last_replied_dmid, 'last_replied_dm.txt')


while True:
    reply_dms()
    time.sleep(15)
