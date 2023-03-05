import requests
import string
import os

from bs4 import BeautifulSoup

table = str.maketrans(dict.fromkeys(string.punctuation))
N = int(input())
pages_title = input()

for i in range(N):
    os.mkdir(f'Page_{i + 1}')
    req = requests.get(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i+1}',
                       headers={'Accept-Language': 'en-US,en;q=0.5'})
    sear = BeautifulSoup(req.content, 'html.parser')
    articles = sear.find_all('article')

    for x in articles:
        article_types = x.find('span', {'data-test': 'article.type'})
        if pages_title == article_types.text.strip():
            article_links = x.find('a', {'data-track-action': 'view article'})
            new_req = requests.get(f"https://www.nature.com{article_links.get('href')}",
                                   headers={'Accept-Language': 'en-US,en;q=0.5'})
            new_sear = BeautifulSoup(new_req.content, 'html.parser')
            paragraphs = new_sear.find('div', {'class': 'c-article-body main-content'}).text
            title_name = new_sear.find('title').text.translate(table).replace(" ", '_')
            with open(f'Page_{i + 1}/{title_name}.txt', "w+b") as article_file:
                article_file.write(paragraphs.encode())