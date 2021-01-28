"""Prediction of Users based on Tweet Embeddings"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine who is more liketly to say a hypothetical tweet.

    Example run: predict_user("elonmusk", "jackblack", "Gamestonks!!")
    Returns 0 (user0_name: "elonmusk") or 1 (user1_name: "jackblack")
    """

    user0 = User.query.filter(User.name == user0_name).one() # is user0_name
    user1 = User.query.filter(User.name == user1_name).one() # is user1_name
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vertically stack embeddings to create one list of vects
    vects = np.vstack([user0_vect, user1_vects]) # user0_vects on user1_vects

    # collection of labels same length as vects
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))]) # 0 is user0, 1 is user1

    # create logistic regression model and fitting
    log_reg = LogisticRegression().fit(vects, labels)

    # reassigning passed in variable to vectorized version
    hypo_tweet_vects = vectorize_tweet(hypo_tweet_text)

    # formats hypo_tweet_vect and runs prediction, will return 0 or 1
    return log_reg.predict(np.array(hypo_tweet_vects).reshape(1, -1))
