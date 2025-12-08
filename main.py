import galactic_war_api
from galactic_war import GalacticWar
from interface.galactic_war_cli import GalacticWarCLI

def main():
    galactic_war = new_galactic_war()
    run_cli(galactic_war)
    #run_web()

def new_galactic_war():
    """calls api and constructs a new galactic war object"""
    """:returns: a galactic_war object"""
    galactic_war_json = galactic_war_api.request_galactic_war_sum_api()
    galactic_war_api.save_galactic_war_sum_to_file(galactic_war_json)
    galactic_war_json = galactic_war_api.read_galactic_war()
    read_planets = galactic_war_api.read_planets()
    galactic_war = GalacticWar(galactic_war_json, read_planets)
    return galactic_war

def run_cli(galactic_war):
    """creates and displays the command line interface"""
    galactic_war_cli = GalacticWarCLI(galactic_war)
    galactic_war_cli.display_menu()

def run_web():
    """runs the web application"""
    raise RuntimeError("not yet implemented")

if __name__ == "__main__":
    main()