import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import json

def req(url, page):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finding URLs for all matches
    cards = soup.find_all('div', class_='wf-card')
    match_urls = []

    for card in cards:
        matches = card.find_all('a', class_=['wf-module-item', 'match-item'])
        
        for match in matches:
            match_urls.append('https://www.vlr.gg' + match['href'])

    return match_urls

match_urls = []

for page in tqdm(range(1, 476), desc="Scraping pages"): # Hardcoded number of pages, could change in the future
    match_urls += req(f'https://www.vlr.gg/matches/results?page={page}', page)
    time.sleep(2)

with open('match_urls.json', 'w') as f:
    json.dump(match_urls, f)