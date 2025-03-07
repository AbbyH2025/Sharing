from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class SpotifyData(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)

class SteamData(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    metascore = db.Column(db.Integer, nullable=False)

def init_db():
    db.create_all()

def load_json_to_db():
    with open("static/steam.json", "r", encoding="utf-8") as jsonfile:
        steam_data = json.load(jsonfile)
        for row in steam_data:
            steam_entry = SteamData(
                id=row["id"],
                title=row["title"],
                release_date=row["release_date"],
                hours=row["hours"],
                metascore=row["metascore"]
            )
            db.session.add(steam_entry)

    with open("static/spotify.json", "r", encoding="utf-8") as jsonfile:
        spotify_data = json.load(jsonfile)
        for row in spotify_data:
            spotify_entry = SpotifyData(
                id=row["id"],
                title=row["title"],
                release_date=row["release_date"],
                album=row["album"],
                artist=row["artist"]
            )
            db.session.add(spotify_entry)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
        load_json_to_db()
