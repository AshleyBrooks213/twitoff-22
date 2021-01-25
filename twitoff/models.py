"""SQLAlchemy models and utility functions for TwitOff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table (Inherting from DB.Model in order to have this be a table)
class User(DB.Model):
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Tweets corresponding to USers"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Tweet text column = allows for emojis
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False) # user_id column (corresponding user)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True)) # creates user link between tweets

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


"""This function creates example users using the User class"""
def insert_example_users():
    nick = User(id=1, name="Nick")
    elon = User(id=2, name="elonmusk")
    DB.session.add(nick)
    DB.session.add(elon)
    DB.session.commit()