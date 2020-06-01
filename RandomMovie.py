
import requests
import xmltodict
import random
from config import *


url = 'http://{}:{}/library/sections/{}/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, MOVIE_SECTION, PLEX_KEY)

response = requests.get(url)
responseDict = xmltodict.parse(response.content)

print(random.choice(responseDict['MediaContainer']['Video'])['@title'])
