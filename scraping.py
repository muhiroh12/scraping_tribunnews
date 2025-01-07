import requests as req
from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter
import re
import json

filename = 'scraping_results2.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
url = 'https://jabar.tribunnews.com/'
response = req.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('li', class_='p1520 art-list pos_rel', limit=10)

article_results = []

def get_most_common_words(text, n=5):
    exceptWords = {
        "dan", "dari", "di", "dengan", "ke", "oleh", "pada", "sejak", "sampai", 
        "seperti", "untuk", "buat", "bagi", "akan", "antara", "demi", "hingga", 
        "kecuali", "tentang", "serta", "tanpa", "kepada", "daripada", "oleh karena itu", 
        "bersama", "beserta", "menuju", "menurut", "sekitar", "selama", "seluruh", 
        "bagaikan", "terhadap", "melalui", "mengenai"
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    
    filtered_words = [word for word in words if word not in exceptWords]
    
    word_counts = Counter(filtered_words)
    most_common_words = [word for word, _ in word_counts.most_common(n)]
    return most_common_words

for i, article in enumerate(articles, 1):
    media = article.find('div', class_='sharecot pos_abs nw')['data-via']
    article_url = article.find('a', class_='f20 ln24 fbo txt-oev-2')['href']
    article_title = article.find('div', class_='mr140').text.strip().replace('\n','').replace('\t','')
    article_release_date = article.find('time', class_='foot timeago')['title']
    category = article.find('a', class_='fbo2 tsa-2')['title']
    images = article.find('img', class_='rd8 shou2 bgwhite')['alt']
    
    response_details = req.get(article_url, headers=headers)
    soup_details = BeautifulSoup(response_details.text, 'html.parser')
    
    content = soup_details.find('div', class_='side-article txt-article multi-fontsize editcontent').text.strip()
    
    most_common_words = get_most_common_words(content, n=5)
    
    article_results.append({
        "scrape_time": scrape_time,
        "media": media,
        "article_release_date": article_release_date,
        "article_title": article_title,
        "article_url": article_url,
        "most_common_words": most_common_words,
        "category": category,
        "images": images
        })
    
with open(filename, 'w') as file:
    json.dump(article_results, file, indent=4)
    
    