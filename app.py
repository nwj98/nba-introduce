from flask import Flask, render_template
from nba_api.stats.static import teams

# http://127.0.0.1:5000 or localhost:5000
app = Flask(__name__)

# category
category = ['teams', 'players', 'careers']

# nba-teams json
nba_teams = teams.get_teams()

# http://127.0.0.1:5000/ or localhost:5000/
@app.route('/')
def index():
    # index.html에 category를 넘겨주는 역할
    return render_template("index.html", categorys=category)

# http://127.0.0.1:5000/teams or localhost:5000/teams
@app.route('/teams')
def teams():
    # teams.html에 category를 넘겨주는 역할
    return render_template('teams.html', teams=nba_teams)


if __name__ == '__main__':
    app.run(debug=True)