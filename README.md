# nba-introduce
nba 선수, 팀, 커리어 소개

# Getting Started
> 1. pip install Flask, pip install nba_api
>2. app.py 파일을 실행시킴
>3. http://127.0.0.1:5000/ or localhost:5000/에 접속
>4. index페이지에서 teams를 누르면 nba팀들을 볼 수 있음
>5. index페이지에서 players를 누르고 선수를 검색하면 선수 정보를 볼 수 있음 // Nikola Jokic
>6. index페이지에서 careers를 누르고 선수를 검색하면 선수 커리어 기록을 볼 수 있음 // Nikola Jokic


# 코드설명

### nba-introduce 시작페이지 용도
```python
# http://127.0.0.1:5000/ or localhost:5000/으로 접속 가능
# 접속하면 teams, players, careers링크 나옴
@app.route('/')
def index():
    # index.html에 category를 넘겨주는 역할
    return render_template("index.html", categorys=category)
```

### nba-team들을 소개하는 페이지
```python
# http://127.0.0.1:5000/teams or localhost:5000/teams로 접속하거나 시작페이지에서 teams를 클릭
# 전체 30개 팀 소개
@app.route('/teams')
def teams():
    # teams.html에 category를 넘겨주는 역할
    return render_template('teams.html', teams=nba_teams)
```

### nba-player를 검색하는 페이지
#### 검색예시 Nikola Jokic
```python
# http://127.0.0.1:5000/players or localhost:5000/players로 접속하거나 시작페이지에서 players를 클릭
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
    # players.html에 search_nba_player를 넘겨주는 역할
    return render_template('players.html', players=search_nba_player)
```
### nba-player의 career를 검색하는 페이지
#### 검색예시 Nikola Jokic
```python
# http://127.0.0.1:5000/careers or localhost:5000/careers로 접속하거나 시작페이지에서 careers를 클릭
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
  # DataFrame값을 html에 테이블로 전달하는 코드
  return render_template('careers.html', players=search_nba_player, tables=[career.to_html(classes='data')], titles=career.columns.values)

```
