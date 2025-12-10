from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import galactic_war_web

app = Flask(__name__, template_folder='templates')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

@app.route('/')
def main():
    """home page"""
    session.clear()
    galactic_war = galactic_war_web.make_galactic_war()
    if not session.get("planets"):
        planets = galactic_war.get_planets_string("")
        session["planets"] = planets
    if not session.get("sectors"):
        sectors = galactic_war.get_sector_string()
        session["sectors"] = sectors
    return render_template('display.html',
                           data=galactic_war.format_galactic_war(), name="Galactic War", sector="")

@app.route('/planets')
def planet_list():
    """presents a list of all planets in the sector or galaxy"""
    sector = request.args.get("sector", "")
    if sector == "":
        planets = session.get("planets")
        message = "All Planets"
    else:
        planets = session.get("planets_in_{}".format(sector))
        message = "Planets In The {} Sector".format(sector)
    session["search_type"] = "planet"
    return render_template('list.html', data=planets, message=message)

@app.route('/sectors')
def sector_list():
    """presents a list of all sectors which, when selected, display a list of planets in the sector"""
    sectors = session.get("sectors")
    session["search_type"] = "sector"
    return render_template('list.html', data=sectors, message="Sectors")

@app.route('/search')
def search():
    """searches for a planet in a list of planets, search by index or name, caps sensitive"""
    galactic_war = galactic_war_web.make_galactic_war()
    query = request.args.get("query", "")
    search_type = session.get("search_type")
    print(query)
    if search_type == "planet":
        if query.isdigit():
            target_planet = galactic_war.index_search(query)
        elif query.isalpha():
            query.lower()
            target_planet = galactic_war.name_search(query)
        else:
            return render_template('error.html', message="Invalid search character!")
        return redirect(url_for('planet', target_planet=galactic_war_web.format_planet(target_planet),
                                planet_name=galactic_war_web.get_planet_name(target_planet),
                                planet_sector=galactic_war_web.get_planet_sector(target_planet)+" Sector"))
    else:
        return None

@app.route('/planet')
def planet():
    """displays the given planet's statistics"""
    target_planet = request.args.get("target_planet", "")
    planet_name = request.args.get("planet_name", "")
    planet_sector = request.args.get("planet_sector", "")
    return render_template('display.html', data=target_planet, name=planet_name, sector=planet_sector)

if __name__ == "__main__":
    app.secret_key = 'squidward'
    app.run()