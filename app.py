from flask import Flask
from flask import render_template, request, redirect
import json
import csv
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import sqlite_utils
app = Flask(__name__)
#https://csvjson.com/csv2json for my csv to json needs
#https://chatgpt.com/share/67a0c918-a9c8-800c-9737-09c42bc42d13
# - I actually have no clue (this is a lie, I have an idea) whats going on and Im trying my best to hold this togeather but it feels like im spiderman keeping that train from falling off the tracks but im not spiderman im some 18yo tranny and Ive got shoestrings 
#   -something something you shouldn't refer to yourself with slurs in a school project but whatever
#   - to quote chapple roan 'my give a fucks are on vaccation'

#sorting most enjoyable playlist.csv by track name alphabeticly so it makes some semblence of sense. Maybe by album title or artists would make more sense but Idk

#spotifyData = pd.read_csv('static/most_enjoyableplaylist.csv')
#sortedSpotifyData = spotifyData.sort_values(by="Track Name")
#print(sortedSpotifyData)



def load_spotify_data():
    spotify_data = []
    with open("static/most_enjoyableplaylist.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spotify_data.append({
                "title": row["Track Name"],
                "id": row.get('\ufeffTrack ID'),
                "release_date": row["Release Date"],
                "album": row["Album Name"],
                "artist": row["Artist Name(s)"]
            })
    spotify_data.sort(key=lambda x: x["title"])
    return spotify_data




def load_steam_data():
    steam_data = []
    with open("static/steam-library-76561198991900225.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            steam_data.append({
                "title": row["game"],
                "id": row["id"],
                "release_date": row["release_date"],
                "hours": row["hours"],
                "metascore": row["metascore"]
            })
    steam_data.sort(key=lambda x: x["hours"])
    return steam_data

def load_top_game():
    with open("static/topGame.json", "r", encoding="utf-8") as jsonfile:
        top_game = json.load(jsonfile)
    return top_game

def load_albums():
    with open("static/topAlbum.json", "r", encoding="utf-8") as jsonfile:
        top_album = json.load(jsonfile)
    return top_album

def load_spotifyWrapped():
    with open("static/SpotifyWrapped.json", "r", encoding="utf-8") as jsonfile:
        spotifyWrapped = json.load(jsonfile)
    return spotifyWrapped

#index route for web app
@app.route("/") 
def index():
    return render_template("index.html")



@app.route("/allSong")
def allSong():
    return render_template("listLayout.html", items=load_spotify_data(), source="spotify")

@app.route("/allGame")
def allGame():
    return render_template("listLayout.html", items=load_steam_data(), source="steam")

@app.route("/spotifyWrapped")
def spotifyWrapped():
    return render_template("gridLayout.html", items=load_spotifyWrapped())

@app.route("/topAlbum")
def topAlbum():
    return render_template("gridLayout.html", items=load_albums(), source="albums")

@app.route("/topGame")
def topGame():
    return render_template("gridLayout.html", items=load_top_game(), source="games")
#finish this, need more routes for everything
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
