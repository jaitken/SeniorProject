from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitterCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pymongo
import json
from pymongo import MongoClient
import time
import datetime
from datetime import timedelta


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitterCredentials.CONSUMER_KEY, twitterCredentials.CONSUMER_SECRET)
        auth.set_access_token(twitterCredentials.ACCESS_TOKEN, twitterCredentials.ACCESS_TOKEN_SECRET)
        return auth


class TweetAnalyzer():
    
    # analyzing and categorizing content from tweets.
    
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

 
if __name__ == '__main__':


    tweet_analyzer = TweetAnalyzer()
    twitter_client = TwitterClient()

    api = twitter_client.get_twitter_client_api()

 




    # hashtag_list = ["delaware"]
    # fecthed_tweets_filename = "tweets.json"
    # twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fecthed_tweets_filename, hashtag_list)

    # TODO: Check for duplicate dictionary entries when enteting input into the DB

    client = MongoClient("mongodb+srv://page_ryan:bi0#52414rp@seniorproject-u3ows.mongodb.net/test?retryWrites=true")
    db = client["DonaldTrump"]
    retweets = db["1069324231333289991"]








    # client = MongoClient("mongodb+srv://page_ryan:bi0#52414rp@seniorproject-u3ows.mongodb.net/test?retryWrites=true")
    # db = client["SeniorProject"]
    # collection = db["KanyeWest"]
    
    # # #formats tweets into 'Status' Objects

    # # #Loops over a collection of 'Status' objects turns -> 'String' Objects -> 'JSON' Objects
    # for status in tweets:
    #     json_str = json.dumps(status._json)
    #     obj = json.loads(json_str)
    #     collection.insert(obj)

    # client.close()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=100)


    #stuff = api.user_timeline(screen_name = twitter_name, count = 100, include_rts = False, tweet_mode = 'extended')


    df = tweet_analyzer.tweets_to_data_frame(tweets)
 
    # Layered Time Series:
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])


    # time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)

    df.plot()

    plt.show()


# END DOCUMENT