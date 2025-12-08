from flask import Flask, render_template
import galactic_war_api
from galactic_war_web import GalacticWarWeb

app = Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    galactic_war = galactic_war_api.new_galactic_war()
    galactic_war_web = GalacticWarWeb(galactic_war)
    return render_template('home.html', message=galactic_war_web.format_galactic_war())

if __name__ == "__main__":
    app.run()