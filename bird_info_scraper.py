import requests
from bs4 import BeautifulSoup
import random
from bing_image_downloader import downloader

bird_index = random.randint(1, 10973)
bird_file = open("birds_list.txt", encoding="utf-8")

bird = ''
for position, line in enumerate(bird_file):
    if position == bird_index:
        bird = line

bird = bird.replace(' ', '_').strip()
url = "https://en.wikipedia.org/wiki/" + bird
print(url)
response = requests.get(
    url=url,
)
soup = BeautifulSoup(response.content, 'html.parser')
data = soup.find_all("p")

overview = ''

for sentence in data:
    sentence = sentence.getText()
    if 'The' in sentence:
        for char in sentence:
            overview += char
            if char == '.':
                break
        break
print(overview)

downloader.download(bird, limit=1, output_dir='bird_photo', adult_filter_off=False, force_replace=False,
                    timeout=60, verbose=True)
