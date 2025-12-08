class GalacticWarWeb:
    def __init__(self, galactic_war):
        self._galactic_war = galactic_war
        self._galactic_war_stats = self._galactic_war.calculate_helldiver_stats()
        self._galactic_war_mission_stats = self._galactic_war.calculate_mission_stats(self._galactic_war_stats)

    def format_galactic_war(self):
        return self._galactic_war.format_galaxy_stats(self._galactic_war_stats, self._galactic_war_mission_stats)