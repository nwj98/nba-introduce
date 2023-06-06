from flask import Flask, render_template, request
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

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


@app.route('/careers', methods=["GET", "POST"])
def careers():
    # careers.html에서 입력받은 값을 가져옴
    search_nba_player = {}
    if request.method == 'POST':
        full_name = request.form['full_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # 입력값과 일치하는 선수를 careers.html에 전달
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
    
    career = pd.DataFrame()
    # 검색된 선수가 존재 할 때
    if search_nba_player != {}:
        # 검색된 선수 id를 이용하여 선수 커리어 DataFrame 생성
        career = playercareerstats.PlayerCareerStats(
            player_id=search_nba_player['id']).get_data_frames()[0]
        career.rename(columns={'PLAYER_ID': 'PLAYER_NAME'}, inplace=True)   # 기존 DataFrame Column 이름 변경
        career.rename(columns={'TEAM_ID': 'TEAM_NAME'}, inplace=True)       # 기존 DataFrame Column 이름 변경
        career.drop(['LEAGUE_ID'], axis=1, inplace=True)                    # 기존 DataFrame Column 삭제
        # PLAYER_ID로 되어있던 값을 선수 이름으로 변경
        for player in nba_players:
            if player['id'] == search_nba_player['id']:
                career.loc[career['PLAYER_NAME'] == search_nba_player['id'],
                           'PLAYER_NAME'] = player['full_name']
                break
        # TEAM_ID로 되어있던 값을 팀 이름으로 변경
        for team in nba_teams:
            career.loc[career['TEAM_NAME'] == team['id'],
                       'TEAM_NAME'] = team['full_name']
    return render_template('careers.html', players=search_nba_player, tables=[career.to_html(classes='data')], titles=career.columns.values)


if __name__ == '__main__':
    app.run(debug=True)
