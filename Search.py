from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import time
import tweepy
from datetime import datetime
import pytz
import whitelistUtil as wu



#Makes the time acctually esaily readable ex: "06:09 PM Oct-31"
def parseTime(time=None):
    fmt = "%I:%M %p %b-%d"
    return time.strftime(fmt)

#Read 'detWhitelistedTweets() comments to understand the code; its basically the same thing- without the whitelist for loop'
def getNonWhitelistedTweets(api, pRawQuery):
    data = " "
    easternTimezone = pytz.timezone('US/Eastern')
    utcTimezone = pytz.timezone('UTC')

    tweets = tweepy.Cursor(api.search, q=pRawQuery, lang="en").items(3)
    for tweet in tweets:
        status = api.get_status(tweet.id ,tweet_mode="extended")
        if tweet.text.split(" ")[0] == "RT":
            pass
        else:
            rawTweetTime = datetime.strptime(str(tweet.created_at), "%Y-%m-%d %H:%M:%S")
            convTweetTime = utcTimezone.localize(rawTweetTime)
            tweetTime = parseTime(convTweetTime.astimezone(easternTimezone))
            scrnName = tweet.user.screen_name
            tweetText = status.full_text     
            linkText = tweetText.split(" ")[-1]
            
            if  linkText[0:4] == "http":
                data += f"<u>@{scrnName}</u> </br> {tweetText} </br> {tweetTime} </br> <a href={linkText}>Link</a>"+"</br></br>"
            else:
                data += f"<u>@{scrnName}</u> </br> {tweetText} </br> {tweetTime} </br></br>"                     

    return data


#Gets the **LATEST** tweets from the users specified in the whitelist, then returns a concatenated string, with html tags, for Flask web 
def getWhitelistedTweets(api, pRawQuery):
    #Final var, will be concatenated and returned
    data = " "
    easternTimezone = pytz.timezone('US/Eastern')
    utcTimezone = pytz.timezone('UTC')

    #the only people whos' tweets will be returned
    whitelists = wu.readTwitterWhitelist()
    ##User given query, it is raw currently, because it needs some formatting to search for specif users, ex) "$TSLA from:DeItaOne"
    
    for whitelist in whitelists:
        #formats the search query to make it only from people in whitelist
        formattedSearch = pRawQuery + f" from:{whitelist}"
        #Searches and gets the 2 latest tweets, from the given query
        tweets = tweepy.Cursor(api.search, q=formattedSearch, lang="en").items(3)
        
        for tweet in tweets:
            #Makes the tweet in "extened mode", whichs makes it not truncated, and shows the FULL tweet.
            status = api.get_status(tweet.id ,tweet_mode="extended")
            
            #We dont want retweets, so checking if the first character is "RT" signifying it is a retweet           
            if tweet.text.split(" ")[0] == "RT":
                pass
            else:
                for name in whitelists:
                    if tweet.user.screen_name == name:
                        #Gets the time the tweet was tweeted, and formats it for later parsing
                        rawTweetTime = datetime.strptime(str(tweet.created_at), "%Y-%m-%d %H:%M:%S")
                        #converted to UTC
                        convTweetTime = utcTimezone.localize(rawTweetTime)
                        #Finally converted to EST
                        tweetTime = parseTime(convTweetTime.astimezone(easternTimezone))
                        #Gets the screen name of the tweeter
                        scrnName = tweet.user.screen_name
                        #The full un-truncated text
                        tweetText = status.full_text     
                        #getting the link from the tweet (if there is one like a news page)
                        linkText = tweetText.split(" ")[-1]
                        #checking is there is a link, if so, html <a> tag will be added to make the link clickable  
                        
                        if  linkText[0:4] == "http":
                            data += f"<u>@{scrnName}</u> </br> {tweetText} </br> {tweetTime} </br> <a href={linkText}>Link</a></br></br>"
                            #If no link, then the <a> tag wont be added.
                        else:
                            data += f"<u>@{scrnName}</u> </br> {tweetText} </br> {tweetTime} </br></br>"                    
                    else:
                        pass
    return data

#Gets the latest tweets from the "scName" specified.                
def tWhite(api):
    scName = ["realDonaldTrump", "MarketWatch", "DeItaOne"]
    for x in scName:
        tweets = api.user_timeline(screen_name = x)
        print(tweets[0].user.screen_name)
        print(tweets[0].text)
        print(parseTime(tweets[0].created_at))
        print("_" *100)

#Twitter main function, has all the secrets and keys to authenticate.
def twitter(pWhitelistChoice ,searchQuery): 
    try:
        #Enter your twitter auth codes here.
        consumerKey = ""
        consumerSecret = ""
        accessToken = ""
        accessSecret = ""

        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        if pWhitelistChoice == "Whitelist":
            data = getWhitelistedTweets(api, searchQuery)
            return data
        else:
            data = getNonWhitelistedTweets(api, searchQuery)
            return data
    except Exception as e:
        print("Authentication Failed... No Twitter results will be shown.")
        print(e)
        return "oof"