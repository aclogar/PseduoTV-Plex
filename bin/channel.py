import json

data = []

class Channel:
    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)

        self.title = self.data["title"]
        self.description = self.data["description"]

    def getGeneralParams(self):
        return self.data["general"]
        
    def getChannel(self, path):
        return data


channel = Channel("channels/tv_tokyo.json")
print (channel.getGeneralParams())
print ( channel.title)
