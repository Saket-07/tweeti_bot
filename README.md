
<a href="https://twitter.com/HeyTweeti"><img alt="![Unable to load image]" src="https://github.com/Saket-07/twitter_bot/blob/main/Images/circle-cropped.png?raw=true" width="125"></a>
# [Tweeti Bot | @HeyTweeti](https://twitter.com/HeyTweeti)

## Description and Features
Tweeti is an interactive bot which can perform certain tasks on Twitter. Following is a brief summary of how this bird-loving birdie tends to calm your hasty twitter feed and help you out...
### Updating the feed
* Get to know about a new bird daily - Everyday, Tweeti randomly picks up a bird and tweets a brief overview along with an enchanting photo of the bird.
* Every once in a while, Tweeti retweets some bird-related post.
### Communicating with users
To talk to our birdie, all you need to do is to mention it in your tweet. It responds to its name at the first call. Following are a few examples of how you can efficiently communicate with it.
* Tweeti can respond to greetings like hi, hello, what's up, etc. It's witty replies might interest you too. Here's an illustration of what to tweet:
```
@HeyTweeti wassup there
```
* Tweeti keeps a track of weather everywhere... this helps it to plan its flight. To know the weather conditions of your city, use the following format, and it will reply you back with the weather description, temperature and humidity at your place:
```
@HeyTweeti city_name weather
```
* You can ask Tweeti to tell you a joke. (Your tweet must contain the keyword 'joke' in it)
```
@HeyTweeti I am bored, do you remember any joke?
```
* Tweeti can help you with some interesting recommendations about books and movies. All you need to do is to call it and request for it (Technically you need to include the subject in your tweet. For say if you want some recommendations for books, you need to include 'book' in your tweet. Same goes for the keyword 'movie')
```
@HeyTweeti suggest me some good movies
```
```
@HeyTweeti I want to read a book
```
* Tweeti is always keen to spread a word about different birds in the world. Feel free to ask about it in the following format:
```
@HeyTweeti bird info bird_name
```
Even if the bird_name you provided does not exactly match with any bird, Tweeti will try its best to tweet about the closest sounding bird.
* You can make Tweeti follow and unfollow you in the following manner:
```
@HeyTweeti follow me
```
```
@HeyTweeti unfollow me
```
(Technically, you can use any commands of your choice, as long as it contains the keyword 'follow me' or 'unfollow me' in it)

## Technical Description
We have used a few API's in order to accomplish certain tasks. Some of them are public API's while others require private API keys in order to be used. Following is a brief description of the API's used:
* Twitter API - A private API used to gain access to various twitter functionalities such as posting a tweet, replying to mentions, etc.
* Jokes API - A public API which returns a random joke on each call.
* Weather API - A private API which returns weather conditions of a city.

Apart from API's, we have implemented web scraping to extract information from various web sources like wikipedia, bing-image search, book recommendations and movie recommendations.

## Tech-stack
* Python 3.9 or above
* Git

## Local Hosting Instructions
* Generate twitter API keys on https://developer.twitter.com/en
* Generate weather API key on https://openweathermap.org/api
* Clone the remote reopsitory on your system.
```
git clone https://github.com/Saket-07/twitter_bot.git
```
* Install all the dependencies by running the command:
```
pip install -r requirements.txt
```
* Now create a '.env' file. Use the following format:
```
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
ACCESS_KEY = 'your_access_key'
ACCESS_SECRET = 'your_access_secret'

WEATHER_API_KEY = 'your_weather_api_key'
```
* Run the following scripts simultaneously on your system:
```
python bird_info_scraper.py
```
```
python bird_retweet.py
```
```
python botsrc.py
```
* Run the following commands in python console:
```
import nltk
```
```
nltk.download("punkt")
```
The project is now up and running on the local server.

Feedbacks are welcome through the direct messages to the bot's twitter account.
