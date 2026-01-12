"""run this file to launch the site locally"""
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import galactic_war_web as galactic_war_web

app = Flask(__name__, template_folder='templates')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

@app.route('/')
def main():
    """home page"""
    session.clear()
    galactic_war = galactic_war_web.make_galactic_war()
    planets = galactic_war.get_planets("")
    session["planets"] = galactic_war_web.get_planets_string(planets)
    session["planet_count"] = len(planets)
    sectors = galactic_war.get_sector_string()
    session["sectors"] = sectors
    session["sector_count"] = galactic_war.get_sector_count()
    return render_template('display.html',
                           data=galactic_war.format_galactic_war(), name="Galactic War", sector="")

@app.route('/planets')
def planet_list():
    """presents a list of all planets in the sector or galaxy"""
    sector = request.args.get("sector", "")

    if sector == "":
        planets = session.get("planets")
        message = "{} Planets".format(session.get("planet_count"))
    else:
        planets = session.get("planets_in_{}".format(sector))
        message = "{} Planets In The {} Sector".format(len(planets),sector)
    session["search_type"] = "planet"
    return render_template('list.html', data=planets, message=message)

@app.route('/sectors')
def sector_list():
    """presents a list of all sectors which, when selected, display a list of planets in the sector"""
    sectors = session.get("sectors")
    session["search_type"] = "sector"
    message = "{} Sectors".format(session.get("sector_count"))
    return render_template('list.html', data=sectors, message=message)

@app.route('/search')
def search():
    """searches for a planet in a list of planets, search by index or name, caps sensitive"""
    galactic_war = galactic_war_web.make_galactic_war()
    query = request.args.get("query", "")
    search_type = session.get("search_type")
    if search_type == "planet":
        query = query.title()
        target_planet = galactic_war.planet_name_search(query)
        if target_planet and len(target_planet) > 1:
            planets = []
            for i in target_planet:
                planets.append(i)
            session["planet_count"] = len(planets)
            planets_str = galactic_war_web.get_planets_string(planets)
            session["planets"] = planets_str
            return redirect('/planets')
        elif target_planet:
            target_planet = target_planet[0]
        if target_planet:
            return redirect(url_for('planet', target_planet=galactic_war_web.format_planet(target_planet),
                                    planet_name=galactic_war_web.get_planet_name(target_planet),
                                    planet_sector=galactic_war_web.get_planet_sector(target_planet)+" Sector"))
        else:
            return render_template('error.html', message="Planet not found!")
    elif search_type == "sector":
        query = query.title()
        target_sector = galactic_war.sector_name_search(query)
        if target_sector:
            planets = galactic_war.get_planets(target_sector)
            session["planets"] = galactic_war_web.get_planets_string(planets)
            session["planet_count"] = len(planets)
            session["sector"] = target_sector
            return redirect('/planets')
        else:
            return render_template('error.html', message="Sector not found!")
    else:
        return render_template('error.html', message="Invalid search type!")

@app.route('/planet')
def planet():
    """displays the given planet's statistics"""
    target_planet = request.args.get("target_planet", "")
    planet_name = request.args.get("planet_name", "")
    planet_sector = request.args.get("planet_sector", "")
    if target_planet != "" and planet_name != "" and planet_sector != "":
        return render_template('display.html', data=target_planet, name=planet_name, sector=planet_sector)
    else:
        return render_template('error.html', message="Invalid planet!")

if __name__ == "__main__":
    app.secret_key = 'squidward'
    app.run()