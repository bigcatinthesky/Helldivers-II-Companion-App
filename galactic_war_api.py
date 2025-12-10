import json
from galactic_war import GalacticWar
import requests

def new_galactic_war():
    """calls api and constructs a new galactic war object"""
    """:returns: a galactic_war object"""
    galactic_war_json = request_galactic_war_sum_api()
    save_galactic_war_sum_to_file(galactic_war_json)
    galactic_war_json = read_galactic_war()
    planets_json = read_planets()
    galactic_war = GalacticWar(galactic_war_json, planets_json)
    return galactic_war

def request_galactic_war_sum_api():
    response = requests.get("https://api.live.prod.thehelldiversgame.com/api/Stats/war/801/summary")
    galactic_war_json = response.json()
    return galactic_war_json

def save_galactic_war_sum_to_file(galactic_war_json):
    with open('.ignore/galactic_war.json', 'w') as galactic_war_file:
        json.dump(galactic_war_json, galactic_war_file, indent=2)

def read_galactic_war():
    with open('.ignore/galactic_war.json', 'r') as galactic_war_file:
        galactic_war_json = json.load(galactic_war_file)
        return galactic_war_json

def read_planets():
    with open('planets.json', 'r') as planets_file:
        planets_json = json.load(planets_file)
        return planets_json