import requests
import wget
from config import *
import json
import xmltodict
import os
import ntpath
import utils


def downloadMovies():
    url = 'http://{}:{}/library/sections/4/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    response = requests.get(url)
    responseDict = xmltodict.parse(response.content)

    count = 1

    # Download movies
    for movie in responseDict['MediaContainer']['Video']:
        mediaKey = movie['Media']['Part']['@key']


        fileTitle = movie['@title']
        formattedFileSize = utils.formatSizeInteger(int(movie['Media']['Part']['@size']))
        totalMovies = len(responseDict['MediaContainer']['Video']) + 1

        fileName = utils.getFileNameFromPath(movie['Media']['Part']['@file'])
        # print("File Name = {}".format(fileName))

        newDirPath = JIMS_PLEX_MOVIE_PATH + fileTitle + '/'
        # print("New Dir Path = {}".format(newDirPath))

        newFilePath = newDirPath + fileName
        # print("New File Path = {}".format(newFilePath))
        

        fileExists = os.path.exists(newFilePath.replace('+','_').replace('!','_'))

        if(fileExists):
            print("{} already exists in {}, moving onto next movie".format(fileName, newDirPath))
            count += 1
            continue

        utils.makeFileDirectory(newDirPath)

        print("Downloading {} - Location {} - Size {} - Left to download ({}/{})".format(fileTitle, newFilePath, formattedFileSize, count, totalMovies))

        downloadUrl = 'http://{}:{}{}?download=1&X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, mediaKey, PLEX_KEY)
        utils.downloadMovie(downloadUrl, newDirPath)

        count += 1

def downloadTVShows():
    # Get list of TV shows url
    # url = 'http://{}:{}/library/sections/3/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    # Get list of seasons from a show
    # url = 'http://{}:{}/library/metadata/5991/children?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    # Get list of episodes from season
    # url = 'http://{}:{}/library/metadata/5992/children?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    getShowsURL = 'http://{}:{}/library/sections/3/all?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, PLEX_KEY)

    getShowsResponse = requests.get(getShowsURL)
    responseDict = xmltodict.parse(getShowsResponse.content)


    for show in responseDict['MediaContainer']['Directory']:
        showTitle = show['@title']
        print(showTitle)
        showDirectory = JIMS_PLEX_TV_PATH + showTitle + '/'

        # Make parent folder for the whole show
        utils.makeFileDirectory(showDirectory)

        # Get seasons data
        seasonsKey = show['@key']
        getSeasonsURL = 'http://{}:{}{}?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, seasonsKey, PLEX_KEY)
        
        getSeasonsResponse = requests.get(getSeasonsURL)
        seasonsResponseDict = xmltodict.parse(getSeasonsResponse.content, force_list={'Directory'})

        for season in seasonsResponseDict['MediaContainer']['Directory']:
            if(season['@title'] == 'All episodes' or 'allLeaves' in season['@key']):
                # We disregard the 'All episodes' season since we want to make directories for each season
                continue
            
            seasonTitle = season['@title']
            seasonDirectory = showDirectory + seasonTitle + '/'
            utils.makeFileDirectory(seasonDirectory)

            episodesKey = season['@key']
            getEpisodeURL = 'http://{}:{}{}?X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, episodesKey, PLEX_KEY)

            getEpisodesResponse = requests.get(getEpisodeURL)
            episodesResponseDict = xmltodict.parse(getEpisodesResponse.content, force_list={'Video'})

            for episode in episodesResponseDict['MediaContainer']['Video']:
                # print("{} - {} - {}".format(episodesResponseDict['MediaContainer']['@title1'], seasonTitle, episode['@title']))
                episodeTitle = episode['@title']
                episodeFileName = utils.getFileNameFromPath(episode['Media']['Part']['@file'])
                episodePath = seasonDirectory + episodeFileName
                formattedFileSize = utils.formatSizeInteger(int(episode['Media']['Part']['@size']))
                mediaKey = episode['Media']['Part']['@key']



                fileExists = os.path.exists(episodePath.replace('+','_').replace('!','_'))
                if(fileExists):
                    print("{} already exists, moving on...".format(episodePath))
                    continue

                print("Downloading {} - Location {} - Size {}".format(episodeTitle, episodePath, formattedFileSize))

                downloadUrl = 'http://{}:{}{}?download=1&X-Plex-Token={}'.format(PLEX_IP_ADDRESS, PLEX_PORT, mediaKey, PLEX_KEY)
                utils.downloadMovie(downloadUrl, episodePath)

                





if __name__ == "__main__":
    # getTotalTVSize()
    # getTotalMovieSize()
    try:
        # downloadMovies()
        downloadTVShows()

    except KeyboardInterrupt as e:
        utils.deleteLocalTmpFiles()
        utils.deleteTVTmpFiles(JIMS_PLEX_TV_PATH)


