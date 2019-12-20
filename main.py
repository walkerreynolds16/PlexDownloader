import requests
import wget
from config import *
import json
import xmltodict




def downloadMovie(url, path):
    filename = wget.download(url)
    print(filename)


outFile = open("output.txt", "w")

url = 'http://{}:{}/library/sections/4/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

response = requests.get(url)
responseDict = xmltodict.parse(response.content)

# outFile.write(json.dumps(responseDict))


# Download movies
for movie in responseDict['MediaContainer']['Video']:
    mediaKey = movie['Media']['Part']['@key']

    downloadUrl = 'http://{}:{}{}?download=1&X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, mediaKey, PLEX_KEY)
    downloadMovie(downloadUrl, JIMS_PLEX_MOVIE_PATH)

