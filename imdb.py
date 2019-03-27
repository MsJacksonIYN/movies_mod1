import requests
from bs4 import BeautifulSoup as BS

url = "https://www.imdb.com/search/title?year=2018&title_type=feature&"
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
page = requests.get(url, headers = headers, timeout=5)
page.status_code

soup = BS(page.content, 'html.parser')
print(soup.prettify())

m_content = soup.find('div', class_ = 'lister-item-content')

m_header = m_content.find('h3', class_ = 'lister-item-header')

m_title = m_header.find('a').get_text()
print(m_title)

m_year = m_header.find('span', class_ = 'lister-item-year').get_text()
print(m_year)

m_muted = m_content.find('p', class_ = 'text-muted')

m_certificate = m_muted.find('span', class_ = 'certificate').get_text()
print(m_certificate)

m_runtime = m_muted.find('span', class_ = 'runtime').get_text()
print(m_runtime)

m_genre = m_muted.find('span', class_ = 'genre').get_text().strip()
print(m_genre)

m_ratings = m_content.find('div', class_ = 'ratings-bar')
m_ratings

m_imdb_rating = m_ratings.find('div', class_ = 'ratings-imdb-rating').get_text().strip()
print(m_imdb_rating)

m_metascore = m_ratings.find('div', class_ = 'ratings-metascore').get_text().strip()
print(m_metascore)

m_visible = m_content.find('p', class_ = 'sort-num_votes-visible')
m_visible

m_visible_children = m_visible.findChildren()
m_votes = m_visible_children[1]['data-value']
m_votes

m_gross = m_visible_children[4]['data-value']
m_gross
