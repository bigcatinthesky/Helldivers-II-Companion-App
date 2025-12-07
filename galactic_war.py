
from planet import Planet

class GalacticWar:
    def __init__(self, json_galaxy_stats_dict, json_planets_dict):
        self._galaxy_stats = {
            "missions won": json_galaxy_stats_dict["galaxy_stats"]["missionsWon"],
            "missions lost": json_galaxy_stats_dict["galaxy_stats"]["missionsLost"],
            "mission time": json_galaxy_stats_dict["galaxy_stats"]["missionTime"],
            "bug kills": json_galaxy_stats_dict["galaxy_stats"]["bugKills"],
            "bot kills": json_galaxy_stats_dict["galaxy_stats"]["automatonKills"],
            "squid kills": json_galaxy_stats_dict["galaxy_stats"]["illuminateKills"],
            "shots hit": json_galaxy_stats_dict["galaxy_stats"]["bulletsFired"],
            "shots fired": json_galaxy_stats_dict["galaxy_stats"]["bulletsHit"],
            "casualties": json_galaxy_stats_dict["galaxy_stats"]["deaths"],
            "friendly fires": json_galaxy_stats_dict["galaxy_stats"]["friendlies"]
        }
        self._planets_list = []
        self._sectors =[]
        planet_attributes = []
        planet_stats = []

        for i in json_planets_dict:
            planet_attributes.append(json_planets_dict[i])
        for i in json_galaxy_stats_dict["planets_stats"]:
            planet_stats.append(i)
        attributes_index = 0
        while attributes_index != len(planet_attributes):
            stats_index = 0
            while stats_index != len(planet_stats):
                if attributes_index == planet_stats[stats_index]["planetIndex"]:
                    new_planet = Planet(planet_stats[stats_index], planet_attributes[attributes_index])
                    self.add_sector(new_planet)
                    self._planets_list.append(new_planet)
                stats_index += 1
            attributes_index += 1

    def add_sector(self, planet):
        if planet.get_planet_attributes()["sector"] not in self._sectors:
            self._sectors.append(planet.get_planet_attributes()["sector"])

    def format_galaxy_stats(self, helldiver_stats, mission_stats):
        """:returns: a readable string of all galaxy statistics"""
        """:param: helldiver_stats, a dictionary of helldiver statistics from calculate_helldiver_stats"""
        """:param: mission_stats, a dictionary of mission averages from calculate_mission_stats"""
        return str("Mission Stats:"
                   + "\n\tMissions Won: {}".format(self._galaxy_stats["missions won"])
                   + "\n\tMissions Lost: {}".format(self._galaxy_stats["missions lost"])
                   + "\n\tMission Time: {} minutes".format(round(self._galaxy_stats["mission time"] / 60, 2))
                   + "\n\tTotal Missions: {}".format(mission_stats["total missions"])
                   + "\n\tMission Success Rate: {}%".format(mission_stats["mission success rate"])
                   + "\n\tMission Averages:"
                   + "\n\t\tAverage Rounds Fired Per Mission: {}".format(mission_stats["average shots per mission"])
                   + "\n\t\tAverage Kills Per Mission: {}".format(mission_stats["average kills per mission"])
                   + "\n\t\tAverage Casualties Per Mission: {}".format(mission_stats["average casualties per mission"])
                   + "\n\t\tAverage Friendly Fire Incidents Per Mission: {}".format(mission_stats["average friendlies per mission"])
                   + "\n\t\tAverage Mission Time: {} minutes".format(round(mission_stats["average mission time"] / 60, 2))
                   + "\nHelldiver Stats:"
                   + "\n\tEnemies Killed:"
                   + "\n\t\tTerminids Killed: {}({}%)".format(self._galaxy_stats["bug kills"], helldiver_stats["bug kill rate"])
                   + "\n\t\tAutomatons Killed: {}({}%)".format(self._galaxy_stats["bot kills"], helldiver_stats["bot kill rate"])
                   + "\n\t\tIlluminate Killed: {}({}%)".format(self._galaxy_stats["squid kills"], helldiver_stats["squid kill rate"])
                   + "\n\t\tTotal Enemies Killed: {}".format(helldiver_stats["total kills"])
                   + "\n\tLosses:"
                   + "\n\t\tHelldiver Casualties: {}".format(self._galaxy_stats["casualties"])
                   + "\n\t\tEnemies Killed Per Helldiver Casualty: {}".format(helldiver_stats["kills per casualty"])
                   + "\n\t\tAverage Helldiver Lifespan: {} minutes".format(helldiver_stats["helldiver lifespan"])
                   + "\n\tAccuracy:"
                   + "\n\t\tRounds Fired: {}".format(self._galaxy_stats["shots fired"])
                   + "\n\t\tRounds Hit: {}".format(self._galaxy_stats["shots hit"])
                   + "\n\t\tHelldiver Accuracy: {}%".format(helldiver_stats["accuracy"])
                   + "\n\t\tRounds Per Kill: {}".format(helldiver_stats["shots per kill"])
                   + "\n\t\tAverage Rounds Fired Per Helldiver: {}".format((helldiver_stats["rounds per helldiver"]))
                   + "\n\tFriendly Fire:"
                   + "\n\t\tFriendly Fire Incidents: {}".format(self._galaxy_stats["friendly fires"])
                   + "\n\t\tFriendly Fire Incident Rate: {}%".format(helldiver_stats["friendly fire rate"]))

    def get_planetary_list(self):
        """:returns: a readable list of all planet names and sectors"""
        return self._planets_list

    def get_sectors(self):
        """:returns: a list of all unique sectors"""
        return self._sectors

    def get_planet_index(self, planet):
        """:returns: the index of a given planet"""
        """:raise: ValueError if planet does not found"""
        index = 0
        for i in self._planets_list:
            if i == planet:
                return index
            index += 1
        raise ValueError

    def calculate_helldiver_stats(self):
        """:returns: a dictionary containing calculated new values, accuracy, total_missions, total_kills,
        mission_success_rate, friendly_fire_rate, kills_per_casualty"""
        accuracy = round((self._galaxy_stats["shots hit"] / self._galaxy_stats["shots fired"]) * 100, 2)
        total_kills = (self._galaxy_stats["bug kills"] + self._galaxy_stats["bot kills"]
                       + self._galaxy_stats["squid kills"])
        bug_kill_rate = round((self._galaxy_stats["bug kills"] / total_kills) * 100, 2)
        bot_kill_rate = round((self._galaxy_stats["bot kills"] / total_kills) * 100, 2)
        squid_kill_rate = round((self._galaxy_stats["squid kills"] / total_kills) * 100, 2)
        friendly_fire_rate = round((self._galaxy_stats["friendly fires"]
                                    / self._galaxy_stats["casualties"]) * 100, 2)
        kills_per_casualty = round(total_kills / self._galaxy_stats["casualties"], 2)
        shots_per_kill = round((self._galaxy_stats["shots fired"] / total_kills), 2)
        helldiver_lifespan = round((self._galaxy_stats["mission time"] / self._galaxy_stats["casualties"]) / 60, 2)
        rounds_fired_per_helldiver = round(self._galaxy_stats["shots fired"] / self._galaxy_stats["casualties"], 2)
        helldiver_stats = {
            "accuracy": accuracy,
            "total kills": total_kills,
            "bug kill rate": bug_kill_rate,
            "bot kill rate": bot_kill_rate,
            "squid kill rate": squid_kill_rate,
            "friendly fire rate": friendly_fire_rate,
            "kills per casualty": kills_per_casualty,
            "shots per kill": shots_per_kill,
            "helldiver lifespan": helldiver_lifespan,
            "rounds per helldiver": rounds_fired_per_helldiver
        }
        return helldiver_stats

    def calculate_mission_stats(self, helldiver_stats):
        """:param: helldiver_stats a dictionary of galaxy stats, provided by calculate_new_planet_stats"""
        """:returns: a dictionary containing calculated new values total_missions, mission_success_rate,
        avg_shots_per_mission, avg_kills_per_mission, avg_casualties_per_mission, avg_friendlies_per_mission,
        avg_mission_time"""
        total_missions = self._galaxy_stats["missions won"] + self._galaxy_stats["missions lost"]
        mission_success_rate = round((self._galaxy_stats["missions won"] / total_missions) * 100, 2)
        avg_shots_per_mission = round(self._galaxy_stats["shots fired"] / total_missions, 2)
        avg_kills_per_mission = round(helldiver_stats["total kills"] / total_missions, 2)
        avg_casualties_per_mission = round(self._galaxy_stats["casualties"] / total_missions, 2)
        avg_friendlies_per_mission = round(self._galaxy_stats["friendly fires"] / total_missions, 2)
        avg_mission_time = round(self._galaxy_stats["mission time"] / total_missions, 2)
        mission_stats = {
            "average shots per mission" : avg_shots_per_mission,
            "average kills per mission" : avg_kills_per_mission,
            "average casualties per mission" : avg_casualties_per_mission,
            "average friendlies per mission" : avg_friendlies_per_mission,
            "average mission time" : avg_mission_time,
            "total missions": total_missions,
            "mission success rate": mission_success_rate,
        }
        return mission_stats

    def planets_in_sector(self, sector):
        """:returns: a list of all planets in the given sector, if no planets in sector, None"""
        """:param sector: a string corresponding to a sector in the galaxy"""
        planets = []
        for i in self._planets_list:
            if i.get_planet_attributes()["sector"] == sector:
                planets.append(i)
        if len(planets) > 0:
            return planets
        else:
            return None

    def planet_search_by_name(self, name):
        """:returns: list of planet(s) containing the given name in the returned string,
         works on incomplete names, None if no planets found"""
        planets = []
        for i in self._planets_list:
            if name in i.__str__():
                planets.append(i)
        if len(planets) > 0:
            return planets
        else:
            return None

    def planet_search_by_index(self, index):
        """:returns: the planet at the given index"""
        """:param: index, the integer index"""
        """:raises: IndexError if index is not valid """
        if index < len(self._planets_list):
            return self._planets_list[index]
        else:
            raise IndexError
