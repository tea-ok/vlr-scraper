from dotenv import load_dotenv
import urllib.request
from bs4 import BeautifulSoup
from typing import Optional
import time
from tqdm import tqdm
import json
import os

# Load proxy config
load_dotenv()
http = os.getenv('HTTP')
https = os.getenv('HTTPS')
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {
            'http': http,
            'https': https
        }
    )
)

def get_last_page(url: str) -> Optional[int]:
    response = opener.open(url)
    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')

    action_container = soup.find('div', class_='action-container')
    if action_container:
        pages_div = action_container.find('div', class_='action-container-pages')
        if pages_div:
            page_links = pages_div.find_all('a', class_='btn mod-page')
            if page_links:
                return int(page_links[-1].text.strip())
    return None

def req(url: str) -> list[str]:
    response = opener.open(url)
    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')

    # Finding URLs for all matches
    cards = soup.find_all('div', class_='wf-card')
    match_urls = []

    for card in cards:
        matches = card.find_all('a', class_=['wf-module-item', 'match-item'])
        
        for match in matches:
            match_urls.append('https://www.vlr.gg' + match['href'])

    return match_urls

last_page = get_last_page('https://www.vlr.gg/matches/results')
match_urls = []

if not last_page:
    print('Error: Could not find last page. Try hardcoding it into the loop in stead.')
else:
    for page in tqdm(range(1, last_page), desc="Scraping pages"):
        match_urls += req(f'https://www.vlr.gg/matches/results?page={page}')
        time.sleep(0.5)

    with open('./data/match_urls.json', 'w') as f:
        json.dump(match_urls, f)