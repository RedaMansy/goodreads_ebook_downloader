import requests
from bs4 import BeautifulSoup

url = "https://www.goodreads.com/review/list/35565370-reda?ref=nav_mybooks&shelf=testshelf"

cached_titles = {}

def extract_book_titles(url):

    try:

        if url in cached_titles:
            print("from cache")
            return cached_titles[url]
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser") 

        # Find all titles and decompose label and span tags
        titles = []
        for title in soup.find_all("td", class_="field title"):
            label = title.find("label")
            if label:
                label.decompose()
            span = title.find("span")
            if span:
                span.decompose()
            title_text = title.text.strip()
            titles.append(title_text)

        cached_titles[title_text] = titles

        return titles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

titles = extract_book_titles(url)
print(titles)
    

def search_for_book(titles):
    zlib = "https://singlelogin.re/s/"
    # zlib = requests.get(zlib)
    # zlib.raise_for_status()
    
    for i in titles:
        search_string = zlib + i
        response = requests.get(search_string)
        soup = BeautifulSoup(response.content, "html.parser")
        links = [a["href"] for a in soup.select('td.itemCover a')]
        print(links[0])
    
search_for_book(titles)
