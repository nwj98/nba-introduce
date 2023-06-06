from flask import Flask, render_template
from nba_api.stats.static import teams

app = Flask(__name__)

# category
category = ['teams', 'players', 'careers']

# nba-teams json
nba_teams = teams.get_teams()

@app.route('/')
def index():
    # index.html에 category를 넘겨주는 역할
    return render_template("index.html", categorys=category)

if __name__ == '__main__':
    app.run(debug=True)