import requests
from bs4 import BeautifulSoup

url = "https://www.goodreads.com/review/list/35565370-reda?ref=nav_mybooks&shelf=testshelf"
zlibrary = "https://singlelogin.re"

cached_titles = {}

def extract_book_titles(url):

    try:
        
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
        print(cached_titles)

        return titles
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

titles = extract_book_titles(url)
print(titles)
    
cached_links = {}

def search_for_book(titles):
    zlib = "https://singlelogin.re/s/"
    # zlib = requests.get(zlib)
    # zlib.raise_for_status()
    if titles in cached_links:
        return cached_links[titles]
    # for i in titles:
    search_string = zlib + titles
    response = requests.get(search_string)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a["href"] for a in soup.select('td.itemCover a')][0]
    cached_links[titles] = links
    print(links)
    return links

book_link = search_for_book("Dune")    

# def extract_download_link(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     download_link = soup.find('a', {'data-target-desktop': 'new-tab'})
#     if download_link:
#         return download_link['href']
#     else:
#         return None
    

# def fetch_html_from_url(book_link):
#     try:
#         url = "https://singlelogin.re/s/"
#         book_link = url + book_link
#         response = requests.get(book_link)
#         response.raise_for_status()
#         print("Response: ", response.text)
#         return response.text
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching URL: {e}")
#         return None


# def download_epub(html_content):
#     content = fetch_html_from_url(html_content)
#     if content:
#         soup = BeautifulSoup(content, 'html.parser')
#         download_link = soup.find('a', {'data-target-desktop': 'new-tab'})
#         if download_link:
#             print (download_link["href"])
#             return download_link['href']
#         else:
#             return None
    

def download_epub(url, filename):
    try:
        # Fetch HTML content from the URL
        # full_url = zlibrary + url
        print(url)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        html_content = response.text

        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        with open("dump.txt", "w") as f:
            f.write(soup) 
        # Find the download button
        download_button = soup.find_all('a', class_='btn btn-primary addDownloadedBook')
        print(download_button)
        if download_button:
            download_url = download_button['href']
            response = requests.get(download_url)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Open a file in binary write mode and write the response content to it
            with open(filename, 'wb') as file:
                file.write(response.content)
            
            print(f"File downloaded successfully: {filename}")
            return True
        else:
            print("Download button not found.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

download_epub("https://singlelogin.re/book/5757113/e330dc/frank-herberts-dune-saga-collection-books-1-6.html", "Dune.epub")

# download_epub("")

# def download_to_files(url, filename):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()

#         with open(filename, "wb") as file:
#             file.write(response.content)
        
#         print(f"File downloaded successfully: {filename}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading file: {e}")

# download_to_files(url, "Dune.epub")