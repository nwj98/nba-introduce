from flask import Flask, render_template, request
from nba_api.stats.static import teams, players

# http://127.0.0.1:5000 or localhost:5000
app = Flask(__name__)

# category
category = ['teams', 'players', 'careers']

# nba-teams json
nba_teams = teams.get_teams()

# nba-player json
nba_players = players.get_players()

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

# http://127.0.0.1:5000/players or localhost:5000/players


@app.route('/players', methods=["GET", "POST"])
def players():
    search_nba_player = {}
    # players.html에서 입력받은 값을 가져옴
    if request.method == 'POST':
        full_name = request.form['full_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # 입력값과 일치하는 선수를 players.html에 전달
        for player in nba_players:
            if player["full_name"] == full_name:
                search_nba_player = player
                break
            elif player["first_name"] == first_name and first_name != '':
                search_nba_player = player
                break
            elif player["last_name"] == last_name:
                search_nba_player = player
                break

    return render_template('players.html', players=search_nba_player)


if __name__ == '__main__':
    app.run(debug=True)
