import requests
import wget
from config import *
import json
import xmltodict
import os



def downloadMovie(url, path):
    filename = wget.download(url)
    print(filename)

def formatSizeInteger(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def downloadMovies():

    # outFile = open("output.txt", "w")

    url = 'http://{}:{}/library/sections/4/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    response = requests.get(url)
    responseDict = xmltodict.parse(response.content)

    # outFile.write(json.dumps(responseDict))

    count = 1

    # Download movies
    for movie in responseDict['MediaContainer']['Video']:
        mediaKey = movie['Media']['Part']['@key']

        fileTitle = movie['@title']
        formattedFileSize = formatSizeInteger(int(movie['Media']['Part']['@size']))
        totalMovies = len(responseDict['MediaContainer']['Video']) + 1

        newDir = makeFileDirectory(JIMS_PLEX_MOVIE_PATH, fileTitle)

        print("Downloading {} - Size {} - Left to download ({}/{})".format(fileTitle, formattedFileSize, count, totalMovies))

        downloadUrl = 'http://{}:{}{}?download=1&X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, mediaKey, PLEX_KEY)
        downloadMovie(downloadUrl, newDir)

        count += 1


def makeFileDirectory(directoryPath,fileTitle):
    newDirPath = directoryPath + fileTitle
    try:
        os.mkdir(newDirPath)
    except OSError as e:
        print ("Creation of the directory %s failed" % newDirPath)
        print(e)

    print ("Successfully created the directory %s " % newDirPath)
    return newDirPath

def getTotalMovieSize():
    url = 'http://{}:{}/library/sections/4/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)
    response = requests.get(url)
    responseDict = xmltodict.parse(response.content)

    totalSize = 0

    for movie in responseDict['MediaContainer']['Video']:
        size = int(movie['Media']['Part']['@size'])
        totalSize += size

    print("Total size in movies = {}".format(formatSizeInteger(totalSize)))

def getTotalTVSize():
    url = 'http://{}:{}/library/sections/3/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)
    outFile = open("outputTV.txt", "w")

    response = requests.get(url)
    responseDict = xmltodict.parse(response.content)

    outFile.write(json.dumps(responseDict))

    totalSize = 0

    for movie in responseDict['MediaContainer']['Video']:
        size = int(movie['Media']['Part']['@size'])
        totalSize += size

    print("Total size in movies = {}".format(formatSizeInteger(totalSize)))


if __name__ == "__main__":
    # getTotalTVSize()
    # getTotalMovieSize()
    # downloadMovies()


