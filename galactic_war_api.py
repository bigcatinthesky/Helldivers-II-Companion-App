import json

import requests

def request_galactic_war_sum_api():
    response = requests.get("https://api.live.prod.thehelldiversgame.com/api/Stats/war/801/summary")
    galactic_war_json = response.json()
    return galactic_war_json

def save_galactic_war_sum_to_file(galactic_war_json):
    with open('.ignore/galactic_war.json', 'w') as galactic_war_file:
        json.dump(galactic_war_json, galactic_war_file, indent=2)

def read_galactic_war():
    with open(".ignore/galactic_war.json", "r") as galactic_war_file:
        galactic_war_json = json.load(galactic_war_file)
        return galactic_war_json

def read_planets():
    with open("planets.json", "r") as planets_file:
        planets_json = json.load(planets_file)
        return planets_json