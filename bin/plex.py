from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
import configparser


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
    for video in movies.search(unwatched=True):
        print(video.title)


getUnwatchedMovies()