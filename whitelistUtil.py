import os


twitterFileName = 'twitterWhitelist.txt'
googleFileName = 'googleWhitelist.txt'

def makeFiles():
    if twitterFileName not in os.listdir():
        with open(twitterFileName, 'x') as file:
            print('Twitter whitelist file made')
    
    elif googleFileName not in os.listdir():
        with open(googleFileName, 'x') as file:
            print('Google whitelist file made.')

    else:
        print("All Files Here and Ready to Rock.")

def readGoogleWhitelist():
    if googleFileName in os.listdir():
        with open(googleFileName, 'r') as file:
            return file.read().splitlines()
    else:
        makeFiles()
        return " "

def readTwitterWhitelist():
    if twitterFileName in os.listdir():
        with open(twitterFileName, 'r') as file:
            return file.read().splitlines()
    else:
        makeFiles()
        
def writeGoogleWhitelist(content):
    if content.isspace() or not content:
        print("Empty-- Like space!")
    else:
        if googleFileName in os.listdir():
            with open(googleFileName, 'a') as file:
                file.write(content+"\n")
        else:
            makeFiles()

def writeTwitterWhitelist(content):
    if content.isspace() or not content:
        print("Empty-- Like space!")
    else:
        if twitterFileName in os.listdir():
            with open(twitterFileName, 'a') as file:
                file.write(content+"\n")
        else:
            makeFiles()

def deleteGoogleWhitelist(content):
    with open(googleFileName, 'r') as file:
        whitelists = file.readlines()
        
    with open(googleFileName, 'w') as file:
        for whitelist in whitelists:
            if whitelist.strip('\n') != content:
                file.write(whitelist)

def deleteTwitterWhitelist(content):
    with open(twitterFileName, 'r') as file:
        whitelists = file.readlines()
        
    with open(twitterFileName, 'w') as file:
        for whitelist in whitelists:
            if whitelist.strip('\n') != content:
                file.write(whitelist)


