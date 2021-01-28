"""SQLAlchemy models and utility functions for TwitOff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table (Inherting from DB.Model in order to have this be a table)
class User(DB.Model):
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True) # id column
    name = DB.Column(DB.String, nullable=False) # name column
    newest_tweet_id = DB.Column(DB.BigInteger) # keeps track of newest id per user

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Tweets corresponding to USers"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Tweet text column = allows for emojis
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False) # vectorized tweet
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False) # user_id column (corresponding user)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True)) # creates user link between tweets

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


"""This function creates example users using the User class"""
def insert_example_users():
    jack = User(id=0, name="jackblack")
    elon = User(id=1, name="elonmusk")
    DB.session.add(jack)
    DB.session.add(elon)
    DB.session.commit()