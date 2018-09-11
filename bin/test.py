# import plex

from channel import Channel
channel = Channel("channels/tv_tokyo.json")
print (channel.getGeneralParams())
print ( channel.title)
print (channel.generateSchedule())

def GetAllChannelsTest():
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
            show = shows[0]
            # show = shows[random.randint(0,len(shows)-1)]
            episodes = getEpisodeBlock(plex,genParams['library'],show.title,genParams['show_block'])
            print (episodes)
            print ("Channel: %s\nDescription: %s" % (channel.title, channel.description))
            for e in episodes:
                print ("%s %s: %s\n%s\n" % (e.grandparentTitle, e.seasonEpisode, e.title, e.summary))
