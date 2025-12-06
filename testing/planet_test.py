import json
import unittest
from planet import Planet

class TestPlanet(unittest.TestCase):

    def test_planet_super_earth(self):
        with open("../Final Project/testing/test.json", "r") as galactic_war_file:
            galactic_war_json = json.load(galactic_war_file)
            test_planet_stats_json = galactic_war_json["planets_stats"][0]
        with open("planets.json", "r") as planets_file:
            planets_json = json.load(planets_file)
            test_planet_attributes_json = planets_json["0"]
        test_planet = Planet(test_planet_stats_json, test_planet_attributes_json)
        """testing attributes"""
        self.assertEqual("Super Earth", test_planet.get_planet_attributes()["name"])
        self.assertEqual("Sol", test_planet.get_planet_attributes()["sector"])
        """testing base stats"""
        self.assertEqual(16553678, test_planet._planet_stats["missions won"])
        self.assertEqual(51840209730, test_planet._planet_stats["mission time"])
        self.assertEqual(120548790, test_planet.get_planet_stats()["casualties"])
        """testing helldiver stats"""
        self.assertEqual(94.3, test_planet.calculate_helldiver_stats()["accuracy"])
        self.assertEqual(7998240868, test_planet.calculate_helldiver_stats()["total kills"])
        self.assertEqual(0, test_planet.calculate_helldiver_stats()["bug kill rate"])
        self.assertEqual(0, test_planet.calculate_helldiver_stats()["bot kill rate"])
        self.assertEqual(100, test_planet.calculate_helldiver_stats()["squid kill rate"])
        self.assertEqual(14.33, test_planet.calculate_helldiver_stats()["friendly fire rate"])
        self.assertEqual(66.35, test_planet.calculate_helldiver_stats()["kills per casualty"])
        self.assertEqual(5.15, test_planet.calculate_helldiver_stats()["shots per kill"])
        self.assertEqual(7.17, test_planet.calculate_helldiver_stats()["helldiver lifespan"])
        self.assertEqual(341.46, test_planet.calculate_helldiver_stats()["rounds per helldiver"])
        mission_time = test_planet._planet_stats["mission time"]
        test_planet._planet_stats["mission time"] = 0
        with self.assertRaises(ValueError):
            test_planet.calculate_helldiver_stats()
        test_planet._planet_stats["mission time"] = mission_time
        """testing mission stats"""
        new_planet_stats = test_planet.calculate_helldiver_stats()
        self.assertEqual(18903061, test_planet.calculate_mission_stats(new_planet_stats)["total missions"])
        self.assertEqual(87.57, test_planet.calculate_mission_stats(new_planet_stats)["mission success rate"])
        self.assertEqual(2177.59, test_planet.calculate_mission_stats(new_planet_stats)["average shots per mission"])
        self.assertEqual(423.12, test_planet.calculate_mission_stats(new_planet_stats)["average kills per mission"])
        self.assertEqual(6.38, test_planet.calculate_mission_stats(new_planet_stats)["average casualties per mission"])
        self.assertEqual(0.91, test_planet.calculate_mission_stats(new_planet_stats)["average friendlies per mission"])
        self.assertEqual(2742.42, test_planet.calculate_mission_stats(new_planet_stats)["average mission time"])
        mission_time = test_planet._planet_stats["mission time"]
        test_planet._planet_stats["mission time"] = 0
        with self.assertRaises(ValueError):
            test_planet.calculate_mission_stats(test_planet.calculate_helldiver_stats())
        test_planet._planet_stats["mission time"] = mission_time
        """format tests"""
        self.assertEqual("Name: Super Earth"+"\nSector: Sol", test_planet.__str__())
        super_earth_stats = str("Mission Stats:"
                         +"\n\tMissions Won: 16553678"+"\n\tMissions Lost: 2349383"
                         +"\n\tMission Time: 864003495.5 minutes"+"\n\tTotal Missions: 18903061"
                         +"\n\tMission Success Rate: 87.57%"
                         +"\n\tMission Averages:"
                         +"\n\t\tAverage Rounds Fired Per Mission: 2177.59"+"\n\t\tAverage Kills Per Mission: 423.12"
                         +"\n\t\tAverage Casualties Per Mission: 6.38"
                         +"\n\t\tAverage Friendly Fire Incidents Per Mission: 0.91"
                         +"\n\t\tAverage Mission Time: 45.71 minutes"
                         +"\nHelldiver Stats:"
                         +"\n\tEnemies Killed:"
                         +"\n\t\tTerminids Killed: 11242(0.0%)"+"\n\t\tAutomatons Killed: 1668(0.0%)"
                         +"\n\t\tIlluminate Killed: 7998227958(100.0%)"+"\n\t\tTotal Enemies Killed: 7998240868"
                         +"\n\tLosses:"
                         +"\n\t\tHelldiver Casualties: 120548790"
                         +"\n\t\tEnemies Killed Per Helldiver Casualty: 66.35"
                         +"\n\t\tAverage Helldiver Lifespan: 7.17 minutes"
                         +"\n\tAccuracy:"
                         +"\n\t\tRounds Fired: 41163068380" + "\n\t\tRounds Hit: 38816787532"
                         +"\n\t\tHelldiver Accuracy: 94.3%"+"\n\t\tRounds Per Kill: 5.15"
                         +"\n\t\tAverage Rounds Fired Per Helldiver: 341.46"
                         +"\n\tFriendly Fire:"
                         +"\n\t\tFriendly Fire Incidents: 17279241" +"\n\t\tFriendly Fire Incident Rate: 14.33%")
        mission_averages = test_planet.calculate_mission_stats(new_planet_stats)
        self.assertEqual(super_earth_stats, test_planet.format_planet_stats(new_planet_stats, mission_averages))