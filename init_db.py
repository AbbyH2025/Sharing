import sqlite3
import json

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS spotify_data (
            id TEXT PRIMARY KEY,
            title TEXT,
            release_date TEXT,
            album TEXT,
            artist TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS steam_data (
            id TEXT PRIMARY KEY,
            title TEXT,
            release_date TEXT,
            hours REAL,
            metascore INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def load_json_to_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
#these json files are wrong, fix em
    with open("static/topGame.json", "r", encoding="utf-8") as jsonfile:
        steam_data = json.load(jsonfile)
        for row in steam_data:
            c.execute('''
                INSERT OR REPLACE INTO steam_data (id, title, release_date, hours, metascore)
                VALUES (?, ?, ?, ?, ?)
            ''', (row["id"], row["title"], row["release_date"], row["hours"], row["metascore"]))

    with open("static/SpotifyWrapped.", "r", encoding="utf-8") as jsonfile:
        spotify_data = json.load(jsonfile)
        for row in spotify_data:
            c.execute('''
                INSERT OR REPLACE INTO spotify_data (id, title, release_date, album, artist)
                VALUES (?, ?, ?, ?, ?)
            ''', (row["id"], row["title"], row["release_date"], row["album"], row["artist"]))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    load_json_to_db()
