class Planet:
    def __init__(self, json_planet_stats_dict, json_planet_attributes_dict):
        self._planet_stats = {
            "missions won" : json_planet_stats_dict["missionsWon"],
            "missions lost" : json_planet_stats_dict["missionsLost"],
            "mission time" : json_planet_stats_dict["missionTime"],
            "bug kills" : json_planet_stats_dict["bugKills"],
            "bot kills" : json_planet_stats_dict["automatonKills"],
            "squid kills" : json_planet_stats_dict["illuminateKills"],
            "shots hit" : json_planet_stats_dict["bulletsFired"], #note bullets fired and hit are swapped in json
            "shots fired" : json_planet_stats_dict["bulletsHit"],
            "casualties" : json_planet_stats_dict["deaths"],
            "friendly fires" : json_planet_stats_dict["friendlies"]
        }
        self._planet_attributes = {
            "name": json_planet_attributes_dict["name"],
            "sector": json_planet_attributes_dict["sector"],
        }

    def __str__(self):
        return "Name: {}".format(self._planet_attributes["name"])+"\nSector: {}".format(self._planet_attributes["sector"])

    def format_planet_stats(self, helldiver_stats, mission_stats):
        """:param: helldiver_stats a dictionary of planet stats, provided by helldiver_stats"""
        """:param: mission_stats a dictionary of mission averages, provided by mission_stats"""
        """:returns: a readable string containing all planet statistics"""
        return str("Mission Stats:"
                         +"\n\tMissions Won: {}".format(self._planet_stats["missions won"])
                         +"\n\tMissions Lost: {}".format(self._planet_stats["missions lost"])
                         +"\n\tMission Time: {} minutes".format(round(self._planet_stats["mission time"]/60, 2))
                         +"\n\tTotal Missions: {}".format(mission_stats["total missions"])
                         +"\n\tMission Success Rate: {}%".format(mission_stats["mission success rate"])
                         +"\n\tMission Averages:"
                         +"\n\t\tAverage Rounds Fired Per Mission: {}".format(mission_stats["average shots per mission"])
                         +"\n\t\tAverage Kills Per Mission: {}".format(mission_stats["average kills per mission"])
                         +"\n\t\tAverage Casualties Per Mission: {}".format(mission_stats["average casualties per mission"])
                         +"\n\t\tAverage Friendly Fire Incidents Per Mission: {}".format(mission_stats["average friendlies per mission"])
                         +"\n\t\tAverage Mission Time: {} minutes".format(round(mission_stats["average mission time"]/60, 2))
                         +"\nHelldiver Stats:"
                         +"\n\tEnemies Killed:"
                         +"\n\t\tTerminids Killed: {}({}%)".format(self._planet_stats["bug kills"], helldiver_stats["bug kill rate"])
                         +"\n\t\tAutomatons Killed: {}({}%)".format(self._planet_stats["bot kills"], helldiver_stats["bot kill rate"])
                         +"\n\t\tIlluminate Killed: {}({}%)".format(self._planet_stats["squid kills"], helldiver_stats["squid kill rate"])
                         +"\n\t\tTotal Enemies Killed: {}".format(helldiver_stats["total kills"])
                         +"\n\tLosses:"
                         +"\n\t\tHelldiver Casualties: {}".format(self._planet_stats["casualties"])
                         +"\n\t\tEnemies Killed Per Helldiver Casualty: {}".format(helldiver_stats["kills per casualty"])
                         +"\n\t\tAverage Helldiver Lifespan: {} minutes".format(helldiver_stats["helldiver lifespan"])
                         +"\n\tAccuracy:"
                         +"\n\t\tRounds Fired: {}".format(self._planet_stats["shots fired"])
                         +"\n\t\tRounds Hit: {}".format(self._planet_stats["shots hit"])
                         +"\n\t\tHelldiver Accuracy: {}%".format(helldiver_stats["accuracy"])
                         +"\n\t\tRounds Per Kill: {}".format(helldiver_stats["shots per kill"])
                         +"\n\t\tAverage Rounds Fired Per Helldiver: {}".format((helldiver_stats["rounds per helldiver"]))
                         +"\n\tFriendly Fire:"
                         +"\n\t\tFriendly Fire Incidents: {}".format(self._planet_stats["friendly fires"])
                         +"\n\t\tFriendly Fire Incident Rate: {}%".format(helldiver_stats["friendly fire rate"]))

    def calculate_helldiver_stats(self):
        """:returns: a dictionary containing calculated new values, accuracy, total_kills,
        bug_kill_rate, bot_kill_rate, squid_kill_rate, friendly_fire_rate, kills_per_casualty, shots_per_kill,
        helldiver_lifespan, rounds_fired_per_helldiver"""
        """:raises: ValueError if mission time !> 0"""
        if self._planet_stats["mission time"] > 0:
            accuracy = round((self._planet_stats["shots hit"] / self._planet_stats["shots fired"]) * 100, 2)
            total_kills = (self._planet_stats["bug kills"] + self._planet_stats["bot kills"]
                           + self._planet_stats["squid kills"])
            bug_kill_rate = round((self._planet_stats["bug kills"]/ total_kills) * 100, 2)
            bot_kill_rate = round((self._planet_stats["bot kills"]/ total_kills) * 100, 2)
            squid_kill_rate = round((self._planet_stats["squid kills"]/ total_kills) * 100, 2)
            friendly_fire_rate = round((self._planet_stats["friendly fires"]
                                        / self._planet_stats["casualties"]) * 100, 2)
            kills_per_casualty = round(total_kills / self._planet_stats["casualties"], 2)
            shots_per_kill = round((self._planet_stats["shots fired"] / total_kills), 2)
            helldiver_lifespan = round((self._planet_stats["mission time"] / self._planet_stats["casualties"]) / 60, 2)
            rounds_fired_per_helldiver = round(self._planet_stats["shots fired"] / self._planet_stats["casualties"], 2)
            helldiver_stats = {
                "accuracy" : accuracy,
                "total kills" : total_kills,
                "bug kill rate" : bug_kill_rate,
                "bot kill rate" : bot_kill_rate,
                "squid kill rate" : squid_kill_rate,
                "friendly fire rate" : friendly_fire_rate,
                "kills per casualty" : kills_per_casualty,
                "shots per kill" : shots_per_kill,
                "helldiver lifespan" : helldiver_lifespan,
                "rounds per helldiver" : rounds_fired_per_helldiver
            }
            return helldiver_stats
        else:
            raise ValueError

    def calculate_mission_stats(self, helldiver_stats):
        """:param: new_planet_stats a dictionary of planet stats, provided by calculate_new_planet_stats"""
        """:returns: a dictionary containing calculated new values total_missions, mission_success_rate,
        avg_shots_per_mission, avg_kills_per_mission, avg_casualties_per_mission, avg_friendlies_per_mission,
        avg_mission_time"""
        """:raises: ValueError if mission time !> 0"""
        if self._planet_stats["mission time"] > 0:
            total_missions = self._planet_stats["missions won"] + self._planet_stats["missions lost"]
            mission_success_rate = round((self._planet_stats["missions won"] / total_missions) * 100, 2)
            avg_shots_per_mission = round(self._planet_stats["shots fired"] / total_missions, 2)
            avg_kills_per_mission = round(helldiver_stats["total kills"] / total_missions, 2)
            avg_casualties_per_mission = round(self._planet_stats["casualties"] / total_missions, 2)
            avg_friendlies_per_mission = round(self._planet_stats["friendly fires"] / total_missions, 2)
            avg_mission_time = round(self._planet_stats["mission time"] / total_missions, 2)
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
        else:
            raise ValueError

    def get_planet_stats(self):
        """:returns: _planet_stats"""
        return self._planet_stats

    def get_planet_attributes(self):
        """:returns: _planet_attributes"""
        return self._planet_attributes