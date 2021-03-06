from flask import Flask
from datetime import datetime
from flask import render_template
import re
import sqlite3
from sqlite3 import Error
import configparser


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        initialDBSetup(conn)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

def initialDBSetup(conn):
    sql_channel = 'CREATE TABLE IF NOT EXISTS `CHANNEL` ( `TITLE` TEXT, `DESCRIPTION` TEXT, `PARAMS` BLOB, `LOGO` TEXT )'
    sql_episode = 'CREATE TABLE IF NOT EXISTS `EPISODES` ( `ID` NUMERIC NOT NULL, `TITLE` TEXT, `DESCRIPTION` TEXT, `SHOW_TITLE` TEXT, `EPISODE_NUM` INTEGER, `START_TIME` INTEGER, `DURATION` INTEGER, PRIMARY KEY(`ID`) )'
    c = conn.cursor()
    c.execute(sql_channel)
    c.execute(sql_episode)
    conn.commit()

def setupConfig():
    config = configparser.ConfigParser()
    config['PLEX'] = {'user': '<USER>',
                         'password': '<PASS>',
                         'token': '<TOKEN>',
                         'baseurl': '<baseurl>:32400'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
 
def setup_server():
    app = Flask(__name__)
    create_connection("programming.db")
    # setupConfig()
    print ("starting server")
    return app

app = setup_server()

@app.route("/")
def home():
    return render_template("home.html")

# New functions
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/hello/<name>")
def hello_there(name):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/")
def get_api():
    return render_template(
        "hello_there.html",
        name="API",
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")