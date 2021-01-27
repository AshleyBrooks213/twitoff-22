"""Main app/routing file for Twitoff."""

from os import getenv
from flask import Flask, render_template
from .models import DB, User, insert_example_users
from .twitter import add_or_update_user

def create_app():
    """Creates the Application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False 

    DB.init_app(app) # initializes app

    """
    Creates a specific route within 
    the Application by using decorators
    """
    @app.route('/')
    def root():
        insert_example_users()
        return render_template('base.html', title="Home",
                                user=User.query.all())

    @app.route('/update')
    def update():
        add_or_update_user("elonmusk")
        return_render_template('base.html', title="Home",
                                users=User.query.all())


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="Home")


    return app 