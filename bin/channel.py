import json
data = []

class Channel(dict):

    ONE_MINUTE = 60000
    ONE_HOUR = 60 * ONE_MINUTE
    ONE_DAY = 24 * ONE_HOUR

    def __init__(self, path):
        with open(path) as f:
            self.id = f.name
            self.data = json.load(f)
        
        self.title = self.data["title"]
        self.description = self.data["description"]
        self.library = self.data["library"]
        self.type = self.data["type"]
        self.plot = ""
        try:
            self.plot = self.data["plot"] 
        except:
            pass


    def getGeneralParams(self):
        return self.data["general"]
        
    def getChannel(self, path):
        return data
    def generateSchedule(self,startTime, days=1):
        import plex 
        import random
        import json
        server = plex.getServer()
        # client = server.clients()[0]
        
        searchParams = {}
        # searchParams = self.getGeneralParams()
        episodeList = []
        movies = []

        if self.type == "movie":
            movies = plex.getMovies(server, **searchParams)
            remMovies = []
            if self.plot != '':
                for m in movies:
                    if m.summary.lower().find(self.plot.lower()) == -1:
                        remMovies.append(m)
            for m in remMovies:
                movies.remove(m)            
        
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
                    ep = Episode(e)
                    episodeList.append(ep)
                    duration += ep.duration
                    print (ep.title)
            if self.type == "movie":           
                movie = movies[random.randint(0,len(movies)-1)]
                duration += movie.duration
                print (movie.title)
                episodeList.append(Movie(movie))

        
        return json.dumps(episodeList)
        # return ""


class Episode(dict):
    def __init__(self, episode):
        self.title = episode.title
        self.show_title = episode.grandparentTitle
        self.duration = episode.duration
        self.isWatched = episode.isWatched
        self.index = episode.index
        # self.start_time = episode.start_time
        self.key = episode.key
        self.episode = episode.seasonEpisode


        dict.__init__(self, 
            title=self.title,
            show_title=self.show_title,
            duration=self.duration,
            isWatched=self.isWatched,
            index=self.index,
            # start_time=self.start_time,
            episode=self.episode,
            key=self.key)

class Movie(dict):
    def __init__(self, movie):
        self.title = movie.title
        # self.show_title = movie.grandparentTitle
        self.duration = movie.duration
        self.isWatched = movie.isWatched
        self.year = movie.year
        # self.start_time = movie.start_time
        # self.index = movie.index
        self.key = movie.key
        # self.movie = movie.seasonmovie


        dict.__init__(self, 
            title=self.title,
            # show_title=self.show_title,
            duration=self.duration,
            isWatched=self.isWatched,
            # index=self.index,
            year=self.year,
            # start_time=self.start_time,
            # episode=self.episode,
            key=self.key)


    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, 
    #         sort_keys=True, indent=4)