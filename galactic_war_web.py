import galactic_war_api as galactic_war_api

class GalacticWarWeb:
    def __init__(self, galactic_war):
        self._galactic_war = galactic_war
        self._galactic_war_stats = self._galactic_war.calculate_helldiver_stats()
        self._galactic_war_mission_stats = self._galactic_war.calculate_mission_stats(self._galactic_war_stats)

    def format_galactic_war(self):
        return self._galactic_war.format_galaxy_stats(self._galactic_war_stats, self._galactic_war_mission_stats)

    def get_planets(self, sector):
        if sector == "":
            return self._galactic_war.get_planetary_list()
        else:
            return self._galactic_war.planets_in_sector(sector)

    def get_sector_string(self):
        sectors = self._galactic_war.get_sectors()
        sectors_str = ''
        index = 0
        for i in sectors:
            index += 1
            sector_str = str(i)+" Sector"+"\n--------------------\n"
            sectors_str += sector_str
        return sectors_str

    def get_sector_count(self):
        return len(self._galactic_war.get_sectors())

    def planet_name_search(self, name):
        return self._galactic_war.planet_search_by_name(str(name))

    def sector_name_search(self, name):
        for i in self._galactic_war.get_sectors():
            print(i)
            if str(name) in i:
                return i
        return None

def make_galactic_war():
    """creates and initializes a galactic war object, converts into returned galactic war web object"""
    galactic_war = galactic_war_api.new_galactic_war()
    galactic_war_web = GalacticWarWeb(galactic_war)
    return galactic_war_web

def format_planet(planet):
    if planet.get_planet_stats()["mission time"] > 0 and planet.get_planet_stats()["shots fired"] > 0:
        helldiver_stats = planet.calculate_helldiver_stats()
        mission_stats = planet.calculate_mission_stats(helldiver_stats)
        return planet.format_planet_stats(helldiver_stats, mission_stats)
    else:
        return "No helldiver operations recorded on {}".format(get_planet_name(planet))

def get_planet_name(planet):
    return planet.get_planet_attributes()["name"]

def get_planet_sector(planet):
    return planet.get_planet_attributes()["sector"]

def get_planets_string(planets):
    planets_str = ''
    index = 0
    for i in planets:
        index += 1
        planet_str = i.__str__()+"\n--------------------\n"
        planets_str += planet_str
    return planets_str