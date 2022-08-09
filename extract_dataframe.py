import json
import pandas as pd
from textblob import TextBlob


def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = len(self)
        return statuses_count
        
    def find_full_text(self)->list:
        text = []
        for i in range(len(self)):
            text.append(self.tweets_list[i]["full_text"])
        return text
    
    
    def find_sentiments(self, text)->list:
        polarity = []; subjectivity = []
        polarity = [TextBlob(txt).sentiment.polarity for txt in text]
        subjectivity = [TextBlob(txt).sentiment.subjectivity for txt in text]
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = []
        for i in range(len(self)):
            created_at.append(self.tweets_list[i]["created_at"])
        return created_at

    def find_source(self)->list:
        source = []
        for i in range(len(self)):
            source.append(self.tweets_list[i]["source"])
        return source

    def find_screen_name(self)->list:
        screen_name = []
        for i in range(len(self)):
            screen_name.append(self.tweets_list[i]["screen_name"])
        return screen_name

    def find_followers_count(self)->list:
        followers_count = []
        for i in range(len(self)):
            followers_count.append(self.tweets_list[i]["followers_count"])
        return followers_count

    def find_friends_count(self)->list:
        friends_count = []
        for i in range(len(self)):
            friends_count.append(self.tweets_list[i]["friends_count"])
        return friends_count

    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = []
        for i in range(len(self)):
            favourite_count.append(self.tweets_list[i]["favourite_count"])
        return favourite_count

    
    def find_retweet_count(self)->list:
        retweet_count = []
        for i in range(len(self)):
            retweet_count.append(self.tweets_list[i]["retweet_count"])
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = []
        for words in self.find_full_text().split():
            if words[0]=="#":
                hashtags.append(words)
        return hashtags
        # to count directly from full_text

    def find_mentions(self)->list:
        mentions = []
        for i in range(len(self)):
            mentions.append(self.tweets_list[i]["user_mentions"])
        return mentions

    def find_location(self)->list:
        location = []
        for i in range(len(self)):
            location.append(self.tweets_list[i]['location'])
        return location

                            
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("../covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
