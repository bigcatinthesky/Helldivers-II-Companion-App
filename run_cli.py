import galactic_war_api
from galactic_war_cli import GalacticWarCLI

def main():
    galactic_war = galactic_war_api.new_galactic_war()
    run_cli(galactic_war)

def run_cli(galactic_war):
    """creates and displays the command line interface"""
    galactic_war_cli = GalacticWarCLI(galactic_war)
    galactic_war_cli.display_menu()

if __name__ == "__main__":
    main()