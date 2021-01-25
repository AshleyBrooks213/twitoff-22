"""Main app/routing file for Twitoff."""

from flask import Flask, render_template
from .models import DB, User, insert_example_users

def create_app():
    """Creates the Application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False 

    DB.init_app(app) # initializes app

    """
    Creates a specific route within 
    the Application by using decorators
    """
    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        return render_template('base.html', title="Home",
                                user=User.query.all())

    @app.route('/goodbye')
    def goodbye():
        return "Goodbye, Twitoff!"


    return app 