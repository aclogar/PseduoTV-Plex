from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi import BASE_HEADERS
import configparser
import random


def getToken(user, password):
    account = MyPlexAccount(user,password)
    return account.authenticationToken

def getServerUser(user, password, serverName):
    account = MyPlexAccount(user,password)
    return account.resource(serverName).connect()


def getServer():
    config = configparser.ConfigParser()
    config.read('config.ini')

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

plex = getServer()
print (getEpisodeBlock(plex, 'Anime', 'Samurai Champloo', 2))
# client = getPlayers(plex)[0]
# unwatched = getUnwatchedMovies()
# item = random.choice(unwatched)

# getUnwatchedMovies()