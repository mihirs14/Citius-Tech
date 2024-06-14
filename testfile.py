from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/mihirsampath/Downloads/football-data-27b26-firebase-adminsdk-exo3m-07cf004056.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://football-data-27b26-default-rtdb.firebaseio.com/'
})

app = FastAPI()

class New_player(BaseModel):
    key: str
    value: dict

class Player_stats(BaseModel):
    name: str
    rank: int
    position: str
    date: str
    team: str

class Player_info(BaseModel):
    stats: dict


@app.get("/players")
def get_players():
    players = []
    ref = db.reference("/").get()
    for i in ref:
        players.append(i)
    return players

@app.get("/{player_name}")
def player_details(player_name: str):
    ref = db.reference(player_name).get()
    return ref

@app.post("/")
def add_player(new_player: New_player):
    ref = db.reference("/")
    ref.update({new_player.key: new_player.value})
    return ref.get()

@app.put("/update/{player_name}")
def update_player(player_name: str, player_info: Player_info):
    ref = db.reference(player_name)
    ref.set(player_info.stats)
    return ref.get()

@app.get("/sort/")
def sort():
    players = []
    ref = db.reference("/").get()
    for i in ref:
        players.append({i:ref[i]['date']})
    sorted_people = sorted(players, key=lambda x: x[next(iter(x))], reverse=True)
    return sorted_people