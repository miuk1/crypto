import os
import time
import twint

#list of twitter usernames to scrape data
users = ["scottmelker",
         "100trillionUSD",
         "rektcapital",
         "nebraskangooner",
         "KoroushAK",
         "MacroCRG",
         "TheCryptoDog",
         "Rager",
         "BTC_JackSparrow", "im_goomba", "michael_saylor"]


def getTweet(users, keyword, since, **kwargs):
    """Gets tweets for each users for provided keyword since timeperiod.
        'users' - list of twitter username
        'keyword' - keyword to search
        'since' - specify date and time from where tweets to be scraped from
        'limit' - optional, provide number of tweets to scrape
    """
    
#current timestamp
    timestr = time.strftime("%Y%m%d")

#check if the tweet file exists and delete it to create a new file everytime the function is called   
    if os.path.exists("./" + timestr + "_btc_tweets.csv"):
        os.remove("./" + timestr + "_btc_tweets.csv")

    for user in users:
        c = twint.Config()
        c.Lang = "en"
        c.Limit = kwargs.get('limit', None)
        c.Store_csv = True
        c.Output = "./" + timestr + "_btc_tweets.csv"
        c.Since = since
        c.Username = user
        c.Search = keyword
        c.Hide_output = True
        c.Count = True
        c.Stats = True

        #check if the resume file exists and delete it for next iteration
        if os.path.exists("./resume_files/" + f'resume_{user}.txt'):
            os.remove("./resume_files/" + f'resume_{user}.txt')

        c.Resume = "./resume_files/" + f'resume_{user}.txt'
        twint.run.Search(c)

#function usage
getTweet(users, "BTC", "2020-10-05 15:55:00",limit=200)
