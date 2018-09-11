import json
data = []

class Channel:

    ONE_MINUTE = 60000
    ONE_HOUR = 60 * ONE_MINUTE
    ONE_DAY = 24 * ONE_HOUR

    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)

        self.title = self.data["title"]
        self.description = self.data["description"]
        self.library = self.data["library"]
        self.type = self.data["type"]


    def getGeneralParams(self):
        return self.data["general"]
        
    def getChannel(self, path):
        return data
    def generateSchedule(self, days=1):
        import plex 
        import random
        import json
        server = plex.getServer()
        searchParams = {}
        # searchParams = self.getGeneralParams()
        episodeList = []
        duration = 0
        while duration < self.ONE_DAY * days :
            for d in self.data["general"]:
                if d != 'library' and d != 'show_block':
                    searchParams[d] = self.data["general"][d]
            if self.type == "tv":
                shows = plex.searchShow(server, self.library, **searchParams)
                show = shows[random.randint(0,len(shows)-1)]
                episodes = plex.getEpisodeBlock(server,self.library,show.title,self.data["general"]['show_block'])
                for e in episodes:
                    episodeList.append(Episode(e))
                    duration += e.duration
                    print (e.title)
                
        
        return json.dumps(episodeList)
        # return ""


class Episode(dict):
    def __init__(self, episode):
        self.title = episode.title
        self.show_title = episode.grandparentTitle
        self.duration = episode.duration
        self.isWatched = episode.isWatched
        self.index = episode.index
        self.key = episode.key
        self.episode = episode.seasonEpisode


        dict.__init__(self, 
            title=self.title,
            show_title=self.show_title,
            duration=self.duration,
            isWatched=self.isWatched,
            index=self.index,
            episode=self.episode,
            key=self.key)
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, 
    #         sort_keys=True, indent=4)