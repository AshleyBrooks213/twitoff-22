"""Retrieve Tweets, embeddings, and put them in our database"""
from os import getenv
import tweepy # Allows us to interact with Twitter
import spacy # Vectorize our tweets
from .models import DB, Tweet, User 


TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
    

def add_or_update_user(username):
    try:
        # Create user based on the username passed into the function
        twitter_user = TWITTER.get_user(username)

        # if the User.query.get statement is false, it will move
        # on to the User() statement
        # If True (if the exist) it will update the user, if we get something back
        # then instantiate a new user
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)


        # Add the user to our database
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200, 
            exclude_replies=True,
            include_rts=False, # include retweets
            tweet_mode="Extended",
            since_id=db_user.newest_tweet_id
        ) # A list of tweets from "username"

        # empty tweets list == false, full tweets list == true
        if tweets:
            # updates newest_tweet_id
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # for each tweet we want to create an embedding
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            # Create tweet that will be added to our DB
            db_tweet = Tweet(id=tweet.id, text=tweet.text,
                                vect=vectorized_tweet)
            # append each tweet from "username" to username.tweets
            db_user.tweets.append(db_tweet)
            # add db_tweet to Tweet DB
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else: 
        # commit everything to the database
        DB.session.commit()


def update_all_users():
    """Update al Tweets for all Users in the User table."""
    for user in User.query.all():
        add_or_update_user(user.name)


        
def insert_example_users():
    add_or_update_user("elonmusk")

