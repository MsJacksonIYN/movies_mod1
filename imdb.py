def parse_movie(m_content):
    m = {}

    m_header = m_content.find('h3', class_ = 'lister-item-header')
    m['title'] = m_header.find('a').get_text()
    m['year'] = m_header.find('span', class_ = 'lister-item-year').get_text()
    m['year'] = int(m['year'][1:5])

    m_muted = m_content.find('p', class_ = 'text-muted')
    m['certificate'] = m_muted.find('span', class_ = 'certificate').get_text()
    m['runtime'] = m_muted.find('span', class_ = 'runtime').get_text()
    m['genre'] = m_muted.find('span', class_ = 'genre').get_text().strip()
    m['genre'] = m['genre'].split(', ')

    m_ratings = m_content.find('div', class_ = 'ratings-bar')
    m['imdb_rating'] = float(m_ratings.find('div', class_ = 'ratings-imdb-rating').get_text().strip())
    m['metascore'] = m_ratings.find('div', class_ = 'ratings-metascore').get_text().strip()
    m['metascore'] = int(m['metascore'].split('\n')[0].strip())

    m_visible = m_content.find('p', class_ = 'sort-num_votes-visible')
    m_visible_children = m_visible.findChildren()
    m['votes'] = int(m_visible_children[1]['data-value'])
    m['gross'] = int(m_visible_children[4]['data-value'].replace(',',''))

    return m
