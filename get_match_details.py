import json
import urllib.request
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm
import os
import time

# Load proxy config
load_dotenv()
http = os.getenv('HTTP')
https = os.getenv('HTTPS')
opener = opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {
            'http': http,
            'https': https
        }
    )
)

# Load the URLs from the JSON file
with open('./data/match_urls.json', 'r') as f:
    urls = json.load(f)

def extract_overview(team_div: BeautifulSoup) -> dict:
    # Extract the team's score
    team_score_div = team_div.find('div', class_='score')
    team_score = team_score_div.text.strip() if team_score_div else None

    # Extract the team's name
    team_name_div = team_div.find('div', class_='team-name')
    team_name = team_name_div.text.strip() if team_name_div else None

    # Extract the T-side and CT-side rounds won
    t_side_score_div = team_div.find('span', class_='mod-t')
    t_side_score = t_side_score_div.text.strip() if t_side_score_div else None

    ct_side_score_div = team_div.find('span', class_='mod-ct')
    ct_side_score = ct_side_score_div.text.strip() if ct_side_score_div else None

    team_overview = {
        'name': team_name,
        'score': team_score,
        't_side_score': t_side_score,
        'ct_side_score': ct_side_score
    }

    return team_overview

def extract_player_info(table: BeautifulSoup) -> list[dict]:
    player_info = []

    tbody = table.find('tbody')
    rows = tbody.find_all('tr') if tbody else []

    # Iterate over each row
    for row in rows:
        # Extract player data
        player_data = {}

        player_details_row = row.find('td', class_='mod-player')
        if player_details_row:

            name_div = player_details_row.find('div', class_='text-of')
            player_data['name'] = name_div.text.strip() if name_div else None

            team_code_div = player_details_row.find('div', class_='ge-text-light')
            player_data['team_code'] = team_code_div.text.strip() if team_code_div else None

            country_div = player_details_row.find('i', class_='flag')
            player_data['country'] = country_div.get('title') if country_div else None

        agent_row = row.find('td', class_='mod-agents')
        # Extract the agent's name
        if agent_row:
            agent_img = agent_row.find('img')
            player_data['agent'] = agent_img.get('title') if agent_img else None

        r_stats_row = row.find_all('td')[2]  # Assuming R stats is always the third td - some tds have the same class
        if r_stats_row:
            r_stats_div = r_stats_row.find('span', class_='stats-sq')
            if r_stats_div:
                r_stats = {
                    'both': r_stats_div.find('span', class_='mod-both').text.strip() if r_stats_div.find('span', class_='mod-both') else None,
                    't': r_stats_div.find('span', class_='mod-t').text.strip() if r_stats_div.find('span', class_='mod-t') else None,
                    'ct': r_stats_div.find('span', class_='mod-ct').text.strip() if r_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['r_stats'] = r_stats

        acs_stats_row = row.find_all('td')[3]  # Assuming ACS stats is always the fourth td
        if acs_stats_row:
            acs_stats_div = acs_stats_row.find('span', class_='stats-sq')
            if acs_stats_div:
                acs_stats = {
                    'both': acs_stats_div.find('span', class_='mod-both').text.strip() if acs_stats_div.find('span', class_='mod-both') else None,
                    't': acs_stats_div.find('span', class_='mod-t').text.strip() if acs_stats_div.find('span', class_='mod-t') else None,
                    'ct': acs_stats_div.find('span', class_='mod-ct').text.strip() if acs_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['acs_stats'] = acs_stats

        kill_stats_row = row.find('td', class_='mod-vlr-kills')
        if kill_stats_row:
            kill_stats_div = kill_stats_row.find('span', class_='stats-sq')
            if kill_stats_div:
                kill_stats = {
                    'both': kill_stats_div.find('span', class_='mod-both').text.strip() if kill_stats_div.find('span', class_='mod-both') else None,
                    't': kill_stats_div.find('span', class_='mod-t').text.strip() if kill_stats_div.find('span', class_='mod-t') else None,
                    'ct': kill_stats_div.find('span', class_='mod-ct').text.strip() if kill_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['kill_stats'] = kill_stats

        death_stats_row = row.find('td', class_='mod-vlr-deaths')
        if death_stats_row:
            death_stats_div = death_stats_row.find('span', class_='stats-sq')
            if death_stats_div:
                death_stats = {
                    'both': death_stats_div.find('span', class_='mod-both').text.strip() if death_stats_div.find('span', class_='mod-both') else None,
                    't': death_stats_div.find('span', class_='mod-t').text.strip() if death_stats_div.find('span', class_='mod-t') else None,
                    'ct': death_stats_div.find('span', class_='mod-ct').text.strip() if death_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['death_stats'] = death_stats

        assist_stats_row = row.find('td', class_='mod-vlr-assists')
        if assist_stats_row:
            assist_stats_div = assist_stats_row.find('span', class_='stats-sq')
            if assist_stats_div:
                assist_stats = {
                    'both': assist_stats_div.find('span', class_='mod-both').text.strip() if assist_stats_div.find('span', class_='mod-both') else None,
                    't': assist_stats_div.find('span', class_='mod-t').text.strip() if assist_stats_div.find('span', class_='mod-t') else None,
                    'ct': assist_stats_div.find('span', class_='mod-ct').text.strip() if assist_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['assist_stats'] = assist_stats

        kd_diff_stats_row = row.find('td', class_='mod-kd-diff')
        if kd_diff_stats_row:
            kd_diff_stats_div = kd_diff_stats_row.find('span', class_='stats-sq')
            if kd_diff_stats_div:
                kd_diff_stats = {
                    'both': kd_diff_stats_div.find('span', class_='mod-both').text.strip() if kd_diff_stats_div.find('span', class_='mod-both') else None,
                    't': kd_diff_stats_div.find('span', class_='mod-t').text.strip() if kd_diff_stats_div.find('span', class_='mod-t') else None,
                    'ct': kd_diff_stats_div.find('span', class_='mod-ct').text.strip() if kd_diff_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['kd_diff_stats'] = kd_diff_stats

        kast_stats_row = row.find_all('td')[8]  # Assuming KAST stats is always the ninth td
        if kast_stats_row:
            kast_stats_div = kast_stats_row.find('span', class_='stats-sq')
            if kast_stats_div:
                kast_stats = {
                    'both': kast_stats_div.find('span', class_='mod-both').text.strip() if kast_stats_div.find('span', class_='mod-both') else None,
                    't': kast_stats_div.find('span', class_='mod-t').text.strip() if kast_stats_div.find('span', class_='mod-t') else None,
                    'ct': kast_stats_div.find('span', class_='mod-ct').text.strip() if kast_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['kast_stats'] = kast_stats

        adr_stats_row = row.find_all('td')[9]  # Assuming ADR stats is always the tenth td
        if adr_stats_row:
            adr_stats_div = adr_stats_row.find('span', class_='stats-sq')
            if adr_stats_div:
                adr_stats = {
                    'both': adr_stats_div.find('span', class_='mod-both').text.strip() if adr_stats_div.find('span', class_='mod-both') else None,
                    't': adr_stats_div.find('span', class_='mod-t').text.strip() if adr_stats_div.find('span', class_='mod-t') else None,
                    'ct': adr_stats_div.find('span', class_='mod-ct').text.strip() if adr_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['adr_stats'] = adr_stats

        headshot_stats_row = row.find_all('td')[10]  # Assuming headshot stats is always the eleventh td
        if headshot_stats_row:
            headshot_stats_div = headshot_stats_row.find('span', class_='stats-sq')
            if headshot_stats_div:
                headshot_stats = {
                    'both': headshot_stats_div.find('span', class_='mod-both').text.strip() if headshot_stats_div.find('span', class_='mod-both') else None,
                    't': headshot_stats_div.find('span', class_='mod-t').text.strip() if headshot_stats_div.find('span', class_='mod-t') else None,
                    'ct': headshot_stats_div.find('span', class_='mod-ct').text.strip() if headshot_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['headshot_stats'] = headshot_stats

        fk_stats_row = row.find_all('td')[11]  # Assuming FK stats is always the twelfth td
        if fk_stats_row:
            fk_stats_div = fk_stats_row.find('span', class_='stats-sq')
            if fk_stats_div:
                fk_stats = {
                    'both': fk_stats_div.find('span', class_='mod-both').text.strip() if fk_stats_div.find('span', class_='mod-both') else None,
                    't': fk_stats_div.find('span', class_='mod-t').text.strip() if fk_stats_div.find('span', class_='mod-t') else None,
                    'ct': fk_stats_div.find('span', class_='mod-ct').text.strip() if fk_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['fk_stats'] = fk_stats

        fd_stats_row = row.find_all('td')[12]  # Assuming FD stats is always the thirteenth td
        if fd_stats_row:
            fd_stats_div = fd_stats_row.find('span', class_='stats-sq')
            if fd_stats_div:
                fd_stats = {
                    'both': fd_stats_div.find('span', class_='mod-both').text.strip() if fd_stats_div.find('span', class_='mod-both') else None,
                    't': fd_stats_div.find('span', class_='mod-t').text.strip() if fd_stats_div.find('span', class_='mod-t') else None,
                    'ct': fd_stats_div.find('span', class_='mod-ct').text.strip() if fd_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['fd_stats'] = fd_stats

        fk_diff_stats_row = row.find_all('td')[13]  # Assuming FK-Diff stats is always the fourteenth td
        if fk_diff_stats_row:
            fk_diff_stats_div = fk_diff_stats_row.find('span', class_='stats-sq')
            if fk_diff_stats_div:
                fk_diff_stats = {
                    'both': fk_diff_stats_div.find('span', class_='mod-both').text.strip() if fk_diff_stats_div.find('span', class_='mod-both') else None,
                    't': fk_diff_stats_div.find('span', class_='mod-t').text.strip() if fk_diff_stats_div.find('span', class_='mod-t') else None,
                    'ct': fk_diff_stats_div.find('span', class_='mod-ct').text.strip() if fk_diff_stats_div.find('span', class_='mod-ct') else None
                }
                player_data['fk_diff_stats'] = fk_diff_stats

        player_info.append(player_data)

    return player_info

def scrape_game(game_div: BeautifulSoup) -> dict:
    # Check if the div contains details
    if not game_div.find('div', class_='vm-stats-game-header'):
        return None

    # Find the team_left_div and team_right_div
    team_divs = game_div.find_all('div', class_='team')
    team_left_div, team_right_div = team_divs[0], team_divs[1] if team_divs else (None, None)

    # Extract the game overview
    team_left_overview = extract_overview(team_left_div)
    team_right_overview = extract_overview(team_right_div)

    # Extract the map name and game duration
    map_div = game_div.find('div', class_='map')
    map_name_span = map_div.find('span')
    map_name = map_name_span.text.strip() if map_name_span else None

    game_duration_div = map_div.find('div', class_='map-duration')
    game_duration = game_duration_div.text.strip() if game_duration_div else None

    # Extract player info
    player_tables = game_div.find_all('table', class_='wf-table-inset')
    if len(player_tables) >= 2:
        team_left_players = extract_player_info(player_tables[0])
        team_right_players = extract_player_info(player_tables[1])
    else:
        team_left_players = None
        team_right_players = None

    game_data = {
        'map': {
            'name': map_name,
            'duration': game_duration
        },
        'team_left': {
            'team_overview': team_left_overview,
            'players': team_left_players
        },
        'team_right': {
            'team_overview': team_right_overview,
            'players': team_right_players
        }
    }

    return game_data

def scrape_match(url: str) -> dict:
    response = opener.open(url)
    if response.status != 200:
        return None
    else:
        content = response.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Basic data
    super_div = soup.find('div', class_='match-header-super')
    event_a = super_div.find('a', class_='match-header-event') if super_div else None
    inner_div = event_a.find('div') if event_a else None
    event_divs = inner_div.find_all('div') if inner_div else None
    event_name = event_divs[0].text.strip() if event_divs and len(event_divs) > 0 else ''
    event_series = event_divs[1].text.strip() if event_divs and len(event_divs) > 1 else ''

    match_header_vs_div = soup.find('div', class_='match-header-vs')
    team_names = [div.text.strip() for div in match_header_vs_div.find_all('div', class_='wf-title-med')] if match_header_vs_div else [None, None]

    scoreline_div = soup.find('div', class_='match-header-vs-score')
    winner_score_element = scoreline_div.find('span', class_='match-header-vs-score-winner')
    winner_score = winner_score_element.text.strip() if winner_score_element else ''

    loser_score_element = scoreline_div.find('span', class_='match-header-vs-score-loser')
    loser_score = loser_score_element.text.strip() if loser_score_element else ''
    scoreline = f'{winner_score}:{loser_score}'

    stage_div = soup.find('div', class_='match-header-vs-note')
    stage = stage_div.text.strip() if stage_div else None # Stage, e.g. Final, Semi-final, etc.

    match_type_divs = soup.find_all('div', class_='match-header-vs-note') # Match type, e.g. Best of 3, Best of 5, etc.
    match_type = match_type_divs[1].text.strip() if len(match_type_divs) > 1 else None

    match_header_date_div = soup.find('div', class_='match-header-date')
    date_time_div = match_header_date_div.find_all('div', class_='moment-tz-convert') if match_header_date_div else None
    date = date_time_div[0].text.strip() if date_time_div > 0 else None
    time = date_time_div[1].text.strip() if date_time_div > 1 else None

    # Map-specific details
    stats_container_div = soup.find('div', class_='vm-stats-container')
    game_divs = stats_container_div.find_all('div', class_='vm-stats-game')
    game_data = [scrape_game(div) for div in game_divs if scrape_game(div) is not None]

    match_data = {
        'team_1': team_names[0],
        'team_2': team_names[1],
        'event': event_name,
        'event_series': event_series,
        'scoreline': scoreline,
        'stage': stage,
        'match_type': match_type,
        'date': date,
        'time': time,
        'games': game_data
    }

    return match_data

# Scraping half of the URLs first
half_length = len(urls) // 2
print(f'Scraping {half_length} matches')
urls_to_scrape = urls[:half_length]
data = []

with open('scraped_urls.log', 'a') as log_file:

    for i, url in enumerate(tqdm(urls_to_scrape, desc='Scraping matches')):
        scraped_data = scrape_match(url)
        if scraped_data is None:
            continue

        data.append(scraped_data)
        log_file.write(url + '\n')

        # Save the data every 100 URLs
        if i % 100 == 0 and i > 0:
            with open('scraped_data.json', 'a') as data_file:
                for item in data:
                    json.dump(item, data_file)
                    data_file.write('\n')
                data = []
        time.sleep(0.5)

    if data:
        with open('scraped_data.json', 'a') as data_file:
            for item in data:
                json.dump(item, data_file)
                data_file.write('\n')