from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi import BASE_HEADERS
import configparser
import random
from channel import Channel
import os


def getToken(user, password):
    account = MyPlexAccount(user,password)
    return account.authenticationToken

def getServerUser(user, password, serverName):
    account = MyPlexAccount(user,password)
    return account.resource(serverName).connect()


def getServer():
    config = configparser.ConfigParser()
    config.read('config.2.ini')

    baseurl = config['DEFAULT']['baseUrl']
    token = config['DEFAULT']['token']
    # token = 'KHMTGfC4Psoc44BEUp93'
    plex = PlexServer(baseurl, token)
    return plex

def getUnwatchedMovies():
    plex = getServer()
    movies = plex.library.section('Movies')
    unwatchedMovies =  movies.search(unwatched=True)
    # for video in unwatchedMovies:
    #     print(video.title)
    return unwatchedMovies

def getPlayers(plex):
    for client in plex.clients():
        print(client.title)
    return plex.clients()

def playMedia(client, item, offset=None):
    print('Playing: ' + item.title)
    print ('Client: ' + client.title)

    # client.goToMedia(item, **d)
    client.playMedia(item, offset=offset)


def getEpisodeBlock(plex, library, show,blockSize=1):
    episodes = plex.library.section(library).get(show).episodes()
    ep = random.randint(1,len(episodes))
    block = []
    if (ep > len(episodes)-blockSize):
        ep = len(episodes)-blockSize+1
    for x in range (ep,ep+blockSize):
        block.append(episodes[x-1])
    return block

def searchShow( plex, library, **params):
    # library = params["library"]
    results = plex.library.section(library).searchShows(**params)
    return results


plex = getServer()
# searchParams = {}
# searchParams["studio"] = "TV Tokyo"
# channel = searchShow(plex, 'Anime', **searchParams)

indir = 'channels'
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        channel = Channel(indir+'/' +f)
        searchParams = {}
        genParams = channel.getGeneralParams()
        for d in genParams:
            if d != 'library' and d != 'show_block':
                searchParams[d] = genParams[d]
        # library = searchParams['library']
        # del searchParams["library"]
        # del searchParams["show_block"]
        shows = searchShow(plex, genParams['library'], **searchParams)
        show = shows[random.randint(0,len(shows)-1)]
        episodes = getEpisodeBlock(plex,genParams['library'],show.title,genParams['show_block'])
        print (episodes)
        print ("Channel: %s\nDescription: %s" % (channel.title, channel.description))
        for e in episodes:
            print ("%s %s: %s\n%s\n" % (e.grandparentTitle, e.seasonEpisode, e.title, e.summary))



# print (getEpisodeBlock(plex, 'Anime', channel[1].title, 2))

# print (getEpisodeBlock(plex, 'Anime', 'Samurai Champloo', 2))
# client = getPlayers(plex)[0]
# unwatched = getUnwatchedMovies()
# item = random.choice(unwatched)

# getUnwatchedMovies()