import unittest
import json
from galactic_war import GalacticWar

class TestGalacticWar(unittest.TestCase):

    def test_galactic_war(self):
        with open("test.json", "r") as galactic_war_file:
            galactic_war_json = json.load(galactic_war_file)
        with open("planets.json", "r") as planets_file:
            planets_json = json.load(planets_file)
            test_galactic_war = GalacticWar(galactic_war_json, planets_json)

        """testing base stats"""
        self.assertEqual(708641278, test_galactic_war._galaxy_stats["missions won"])
        self.assertEqual(2264323640041, test_galactic_war._galaxy_stats["mission time"])

        """testing helldiver stats"""
        self.assertEqual(88.83, test_galactic_war.calculate_helldiver_stats()["accuracy"])
        self.assertEqual(281107730429, test_galactic_war.calculate_helldiver_stats()["total kills"])
        self.assertEqual(59.04, test_galactic_war.calculate_helldiver_stats()["bug kill rate"])
        self.assertEqual(23.25, test_galactic_war.calculate_helldiver_stats()["bot kill rate"])
        self.assertEqual(17.71, test_galactic_war.calculate_helldiver_stats()["squid kill rate"])
        self.assertEqual(11.71, test_galactic_war.calculate_helldiver_stats()["friendly fire rate"])
        self.assertEqual(44.92, test_galactic_war.calculate_helldiver_stats()["kills per casualty"])
        self.assertEqual(5.00, test_galactic_war.calculate_helldiver_stats()["shots per kill"])
        self.assertEqual(6.03, test_galactic_war.calculate_helldiver_stats()["helldiver lifespan"])
        self.assertEqual(224.39, test_galactic_war.calculate_helldiver_stats()["rounds per helldiver"])

        """testing mission averages"""
        helldiver_stats = test_galactic_war.calculate_helldiver_stats()
        self.assertEqual(777314218, test_galactic_war.calculate_mission_stats(helldiver_stats)["total missions"])
        self.assertEqual(91.17, test_galactic_war.calculate_mission_stats(helldiver_stats)["mission success rate"])
        self.assertEqual(1806.45, test_galactic_war.calculate_mission_stats(helldiver_stats)["average shots per mission"])
        self.assertEqual(361.64, test_galactic_war.calculate_mission_stats(helldiver_stats)["average kills per mission"])
        self.assertEqual(8.05, test_galactic_war.calculate_mission_stats(helldiver_stats)["average casualties per mission"])
        self.assertEqual(0.94, test_galactic_war.calculate_mission_stats(helldiver_stats)["average friendlies per mission"])
        self.assertEqual(2913.01, test_galactic_war.calculate_mission_stats(helldiver_stats)["average mission time"])

        """format tests"""
        galaxy_stats = str("Mission Stats:"
                                + "\n\tMissions Won: 708641278" + "\n\tMissions Lost: 68672940"
                                + "\n\tMission Time: 37738727334.02 minutes" + "\n\tTotal Missions: 777314218"
                                + "\n\tMission Success Rate: 91.17%"
                                + "\n\tMission Averages:"
                                + "\n\t\tAverage Rounds Fired Per Mission: 1806.45" + "\n\t\tAverage Kills Per Mission: 361.64"
                                + "\n\t\tAverage Casualties Per Mission: 8.05"
                                + "\n\t\tAverage Friendly Fire Incidents Per Mission: 0.94"
                                + "\n\t\tAverage Mission Time: 48.55 minutes"
                                + "\nHelldiver Stats:"
                                + "\n\tEnemies Killed:"
                                + "\n\t\tTerminids Killed: 165952721973(59.04%)" + "\n\t\tAutomatons Killed: 65362568662(23.25%)"
                                + "\n\t\tIlluminate Killed: 49792439794(17.71%)" + "\n\t\tTotal Enemies Killed: 281107730429"
                                + "\n\tLosses:"
                                + "\n\t\tHelldiver Casualties: 6257905765"
                                + "\n\t\tEnemies Killed Per Helldiver Casualty: 44.92"
                                + "\n\t\tAverage Helldiver Lifespan: 6.03 minutes"
                                + "\n\tAccuracy:"
                                + "\n\t\tRounds Fired: 1404180556689" + "\n\t\tRounds Hit: 1247269663156"
                                + "\n\t\tHelldiver Accuracy: 88.83%" + "\n\t\tRounds Per Kill: 5.0"
                                + "\n\t\tAverage Rounds Fired Per Helldiver: 224.39"
                                + "\n\tFriendly Fire:"
                                + "\n\t\tFriendly Fire Incidents: 732813145" + "\n\t\tFriendly Fire Incident Rate: 11.71%")
        mission_averages = test_galactic_war.calculate_mission_stats(helldiver_stats)
        self.assertEqual(galaxy_stats, test_galactic_war.format_galaxy_stats(helldiver_stats, mission_averages))

        planets = []
        for i in test_galactic_war._planets_list:
            planets.append(i)
        self.assertEqual(planets, test_galactic_war.get_planetary_list())

        """planet search test"""
        self.assertEqual(test_galactic_war._planets_list[0], test_galactic_war.search_planet_by_index(0))
        planets_with_new_in_name = [planets[4], planets[20], planets[93]]
        self.assertEqual(planets_with_new_in_name, test_galactic_war.search_planet_by_attribute("New"))
        planets_with_squidward_in_name = []
        self.assertEqual(planets_with_squidward_in_name, test_galactic_war.search_planet_by_attribute("squidward"))
        self.assertEqual(0, test_galactic_war.get_planet_index(planets[0]))
        null_planet = None
        with self.assertRaises(ValueError):
            test_galactic_war.get_planet_index(null_planet)