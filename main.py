import requests
import wget
from config import *
import json
import xmltodict
import os
import ntpath


def downloadMovie(url, path):
    filename = wget.download(url, path)
    print(filename)

def formatSizeInteger(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def checkIfFileExists(directory, filename):
    path = directory + filename
    return os.path.exists(path)

def getFileNameFromPath(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def downloadMovies():
    url = 'http://{}:{}/library/sections/4/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    response = requests.get(url)
    responseDict = xmltodict.parse(response.content)

    count = 1

    # Download movies
    for movie in responseDict['MediaContainer']['Video']:
        mediaKey = movie['Media']['Part']['@key']


        fileTitle = movie['@title']
        formattedFileSize = formatSizeInteger(int(movie['Media']['Part']['@size']))
        totalMovies = len(responseDict['MediaContainer']['Video']) + 1

        fileName = getFileNameFromPath(movie['Media']['Part']['@file'])
        # print("File Name = {}".format(fileName))

        newDirPath = JIMS_PLEX_MOVIE_PATH + fileTitle + '/'
        # print("New Dir Path = {}".format(newDirPath))

        newFilePath = newDirPath + fileName
        # print("New File Path = {}".format(newFilePath))
        

        fileExists = os.path.exists(newFilePath.replace('+','_'))

        if(fileExists):
            print("{} already exists in {}, moving onto next movie".format(fileName, newDirPath))
            continue

        makeFileDirectory(newDirPath)

        print("Downloading {} - Location {} - Size {} - Left to download ({}/{})".format(fileTitle, newFilePath, formattedFileSize, count, totalMovies))

        downloadUrl = 'http://{}:{}{}?download=1&X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, mediaKey, PLEX_KEY)
        downloadMovie(downloadUrl, newDirPath)

        count += 1


def makeFileDirectory(newDirPath):
    try:
        os.mkdir(newDirPath)
    except OSError as e:
        print ("Creation of the directory %s failed" % newDirPath)
        print(e)

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

def deleteLocalTmpFiles():
    currPath = os.getcwd()

    listDir = os.listdir(currPath)

    for item in listDir:
        if item.endswith(".tmp"):
            print("File {} being deleted".format(item))
            os.remove(os.path.join(currPath, item))


if __name__ == "__main__":
    # getTotalTVSize()
    # getTotalMovieSize()
    try:
        downloadMovies()

    except KeyboardInterrupt as e:
        deleteLocalTmpFiles()


