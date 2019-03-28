import requests
from bs4 import BeautifulSoup as BS

def get_m_content(year, start):
    url = "https://www.imdb.com/search/title?title_type=feature&year={}-01-01,{}-12-31&start={}&ref_=adv_nxt".format(year, year, start)
    print(url)
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    page = requests.get(url, headers = headers, timeout=5)
    page.status_code
    soup = BS(page.content, 'html.parser')
    m_content = soup.findAll('div', class_ = 'lister-item-content')
    return m_content

import re

def parse_movie(m_content):
    m = {}

    m_header = m_content.find('h3', class_ = 'lister-item-header')
    if m_header.find('a'):
        m['title'] = m_header.find('a').get_text()
    if m_header.find('span', class_ = 'lister-item-year'):
        m['year'] = m_header.find('span', class_ = 'lister-item-year').get_text()
        if m['year']:
            m['year'] = re.findall('\d+', m['year'])

    m_muted = m_content.find('p', class_ = 'text-muted')
    if m_muted.find('span', class_ = 'certificate'):
        m['certificate'] = m_muted.find('span', class_ = 'certificate').get_text()
    if m_muted.find('span', class_ = 'runtime'):
        m['runtime'] = m_muted.find('span', class_ = 'runtime').get_text()
    if m_muted.find('span', class_ = 'genre'):
        m['genre'] = m_muted.find('span', class_ = 'genre').get_text().strip()
        m['genre'] = m['genre'].split(', ')

    m_ratings = m_content.find('div', class_ = 'ratings-bar')
    if m_ratings:
        if m_ratings.find('div', class_ = 'ratings-imdb-rating'):
            m['imdb_rating'] = float(m_ratings.find('div', class_ = 'ratings-imdb-rating').get_text().strip())
        if m_ratings.find('div', class_ = 'ratings-metascore'):
            m['metascore'] = m_ratings.find('div', class_ = 'ratings-metascore').get_text().strip()
            m['metascore'] = int(m['metascore'].split('\n')[0].strip())

    m_visible = m_content.find('p', class_ = 'sort-num_votes-visible')
    if m_visible:
        m_visible_children = m_visible.findChildren()
        if len(m_visible_children)>=2:
            m['votes'] = int(m_visible_children[1]['data-value'].replace(',',''))
            if len(m_visible_children)>=5:
                m['gross'] = int(m_visible_children[4]['data-value'].replace(',',''))

    return m

import time

all_2018_movies = []
for i in list(range(1,10000,50)):
    m_content = get_m_content(2018, i)
    time.sleep(5)
    
    for movie in m_content:
        all_2018_movies.append(parse_movie(movie))
        
all_2018_movies
print(len(all_2018_movies))

all_2019_movies = []
for i in list(range(1,6600,50)):
    m_content = get_m_content(2019, i)
    time.sleep(10)
    
    for movie in m_content:
        all_2019_movies.append(parse_movie(movie))
        
all_2019_movies
print(len(all_2019_movies))

import pandas as pd

df_2018 = pd.DataFrame(all_2018_movies)
df_2018.to_csv('imdb_2018.csv')
df_2018.head()

df_2019 = pd.DataFrame(all_2019_movies)
df_2019.to_csv('imdb_2019.csv')
df_2019.head()