##### Imports #####
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import re
import os


##### Funcitons #####
def blogs_to_dict(url):
    """
    Function takes in a URL that links to a Codeup article,
    returns a dictionary with a tiles, content, and date
    """
    title = []
    content = []
    headers = {'User-Agent': 'Jason-Tellez'} # Some websites don't accept the pyhon-requests default user-agent
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html)
    body = soup.select('.et_pb_column.et_pb_column_3_4.et_pb_column_0_tb_body.et_pb_css_mix_blend_mode_passthrough')
    
    title = soup.title.string

    for p in range(2, len(body[0].select('p'))):
        content.append(body[0].select('p')[p].text)
    content = ' '.join(content).replace('\xa0', ' ').replace('via GIPHY', '').replace('     ', ' ')
    
    string = body[0].select('p')[0].text
    regexp = r'.{,12}'
    date = re.search(regexp, string)[0]
    
    return {'title': title, 'content': content, 'date': date}



def inshort_articles(url):
    """
    Function takes in URL that links to a page showing links to articles with a specific category,
    returns dictionary with title, content, category, and author of article
    """
    headers = {'User-Agent': 'Jason-Tellez'} # Some websites don't accept the pyhon-requests default user-agent

    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html)
    authors = []
    titles = []
    content = []
    articles = soup.select('.card-stack')[0].select('.news-card.z-depth-1')

    for article in range(len(articles)):
        authors.append(soup.find_all("span", {"class": "author"})[::2][article].text)
        titles.append(soup.find_all("span", {"itemprop": "headline"})[article].text)
        content.append(soup.find_all("div", {"itemprop": "articleBody"})[article].text)
    regexp = r'\w*$'
    category = re.findall(regexp, url)[0]
        
    return {'title': titles, 'content':content, 'category': category, 'author':authors}