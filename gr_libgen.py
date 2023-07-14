import requests
from bs4 import BeautifulSoup

url = "https://www.goodreads.com/review/list/35565370?shelf=to-read"

def extract_book_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser") 

    book_titles = soup.find_all("td", class_="field title")
    titles = []
    for i in book_titles:
        i.label.decompose()
        if i.span:
            i.span.decompose()
        titles.append(i.text.strip())
    return titles

titles = extract_book_titles(url)