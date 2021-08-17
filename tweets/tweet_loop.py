from pyfiglet import Figlet
from datetime import timedelta
import twint
import nest_asyncio
import pandas as pd
import glob
import os
import sys
nest_asyncio.apply()



def twint_search(searchterm, since, until, filename, limit):
    """
    Twint search for a specific date range.
    Stores results to json.
    """
    c = twint.Config()
    c.Search = searchterm
    c.Since = since
    c.Lang = 'en'
    c.Until = until
    c.Hide_output = True
    c.Output = filename
    c.Debug = True
    c.Limit = limit

    try:
        twint.run.Search(c)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print(f"Problem with {since}")


def twint_loop(searchterm, since, until, limit):
    """
    Twint search loops through date from since to until.
    Produces a single csv output to final_csv directory
    """
    daterange = pd.date_range(since, until)

    outputfile = "./final_csv/" + since + "_to_" + until + "_"+ searchterm + "_tweets.csv"
    
    #check if the tweet file exists and delete it to create a new file everytime the function is called   
    if os.path.exists(outputfile):
        os.unlink(outputfile)

    #clean up previous scraped files
    for f in glob.glob('scraped_tweets/*.csv'):
        os.unlink (f)

    for start_date in reversed(daterange):
        since = start_date.strftime("%Y-%m-%d")
        until = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")

        filename = "./scraped_tweets/" + since + "_to_" + until + "_"+ searchterm + "_tweets.csv"

        print(f'Getting tweets from {since} to {until}')
        twint_search(searchterm, since, until, filename, limit)
    
    # merging the fils
    joined_list = glob.glob('scraped_tweets/*.csv')
        
    # Finally, the files are joined
    result_obj = pd.concat([pd.read_csv(file, header=None, sep='\n') for file in joined_list])
    result_obj.to_csv(outputfile, index=False, encoding="utf-8")

    return print(f'Tweets saved to file ---> {outputfile}')


if __name__ == "__main__":
    print(f'Running Script {sys.argv[0]}')
    custom_fig = Figlet(font='jazmine')
    print(custom_fig.renderText('Thejeshwoor Scrapper!!!'))

    searchterm = input('Enter tweet keyword to scrape:')

    start_date = input('From when do you want to scrape tweets? Provide date(eg. 2021-05-02)')
    end_date = input('Till when do you want to scrape tweets? Provide date(eg. 2021-05-02)')
    limit = input('How many tweets do you want to scrape in a day? (eg 100, 200)')

    if (len(searchterm) < 1):
        raise ValueError('Where is the keyword? Need it to scrape, ')

    elif (len(start_date) < 1 or len(end_date) < 1):
        raise ValueError('Missing start or end date!!')

    elif (len(limit) < 1):
        raise ValueError('Looks like you did not put any limit! pLease be gentle and provide limit')


    twint_loop(searchterm, start_date, end_date, limit)
