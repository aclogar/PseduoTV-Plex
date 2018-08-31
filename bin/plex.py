from plexapi.myplex import MyPlexAccount

def getToken(user, password):
    account = MyPlexAccount(user,password)
    return account.authenticationToken
