
class GalacticWarCLI:
    def __init__(self, galactic_war):
        self._galactic_war = galactic_war
        self._galactic_war_stats = self._galactic_war.calculate_helldiver_stats()
        self._galactic_war_mission_stats = self._galactic_war.calculate_mission_stats(self._galactic_war_stats)
        self.separator = "\n====================================================================================================\n"

    def display_menu(self):
        do = True
        while do:
            try:
                print(self.separator+"Galactic War Overview")
                print("| Quit(1) | Display Galactic War Summary(2) |  Planet List(3) | Sector List(4) |"+self.separator)
                r = int(input("command: "))
                if r == 1:
                 print("quitting program...")
                 do = False
                elif r == 2:
                    print(self.separator+"Galactic War Summary")
                    print(self._galactic_war.format_galaxy_stats(self._galactic_war_stats, self._galactic_war_mission_stats))
                    print(len(self._galactic_war.get_planetary_list()), "Total Planets"+self.separator)
                    input("press enter to return...")
                elif r == 3:
                    planets = self._galactic_war.get_planetary_list()
                    self.display_planet_list(planets)
                elif r == 4:
                    self.display_sector_list()
                else:
                   input("invalid command...")
            except ValueError:
                input("command must be integer...")

    def display_sector_list(self):
        do = True
        while do:
            try:
                sectors = self._galactic_war.get_sectors()
                index = 0
                while index < len(sectors):
                    print("(", index+1, ")", sectors[index])
                    index += 1
                print(self.separator + str(index + 1), "Total Sectors")
                print("| Return(1) | Select Sector(2) |" + self.separator)
                r = int(input("command: "))
                if r == 1:
                    do = False
                elif r == 2:
                    index = int(input("enter sector index: "))
                    index -= 1
                    if 0 <= index < len(sectors):
                        print(self.separator+sectors[index]+" Sector"+self.separator)
                        self.display_planet_list(self._galactic_war.planets_in_sector(sectors[index]))
                    else:
                        input("index out of range...")
                else:
                    input("invalid command...")
            except ValueError:
                input("command must be and integer...")

    def display_planet_list(self, planets):
        do = True
        while do:
            try:
                index = 0
                print(self.separator + "Planetary List")
                for i in planets:
                    print("(", index+1, ")", i, "\nTotal mission time:", round(i.get_planet_stats()["mission time"] / 60),
                          "minutes")
                    index += 1
                print(self.separator + str(index+1), "Total Planets")
                print("| Return(1) |  Search Planet(2) | Search By Name(3) |"+self.separator)
                r = int(input("command: "))
                if r == 1:
                    do = False
                elif r == 2:
                    planets = self._galactic_war.get_planetary_list()
                    index = int(input("enter planet index: "))
                    index -= 1
                    if 0 <= index < len(planets):
                        planet = self._galactic_war.planet_search_by_index(index)
                        self.display_planet_stats(planet)
                    else:
                        input("index out of range...")
                elif r == 3:
                    planets = self._galactic_war.get_planetary_list()
                    name = str(input("enter planet name:"))
                    planets = self._galactic_war.planet_search_by_name(name)
                    if planets is not None:
                        self.display_planet_list(planets)
                    else:
                        input("no planets found, enter to continue...")
                        do = False
                else:
                    input("invalid command...")
            except ValueError:
                input("command must be and integer...")

    def display_planet_stats(self, planet):
        planet_header = planet.__str__()
        if planet.get_planet_stats()["shots fired"] > 0:
            print(self.separator+planet_header+self.separator)
            print(self.separator+"Planetary Statistics:")
            helldiver_stats = planet.calculate_helldiver_stats()
            mission_stats = planet.calculate_mission_stats(helldiver_stats)
            print(planet_header, "\n", planet.format_planet_stats(helldiver_stats, mission_stats)+self.separator)
            input("enter to continue...")
        else:
            print(self.separator+planet_header)
            input("no recorded helldiver operations on planet...")