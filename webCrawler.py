import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

def getLinks(html, base_url):
    links = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('a')
        for tag in tags:
            link = tag.get('href')
            if link:
                # Converte URLs relativas em URLs absolutas
                absolute_link = urljoin(base_url, link)
                links.append(absolute_link)
    except Exception as e:
        print(f"Error while parsing HTML: {e}")
    return links

def main(start_url):
    toCrawl = [start_url]
    crawled = set()

    while toCrawl:
        url = toCrawl.pop(0)  # Use pop(0) para BFS
        if url in crawled:  # Evite recrawling
            continue

        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se há erros HTTP
            html = response.text
            links = getLinks(html, url)  # Passe a URL base para tratar links relativos

            if links:
                for link in links:
                    if link not in crawled and link not in toCrawl:
                        toCrawl.append(link)

            print(f'Crawling {url}')
            crawled.add(url)

        except requests.exceptions.RequestException as e:
            print(f"Failed to crawl {url}: {e}")

    if not toCrawl:
        print('No more links to crawl.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Web Crawler")
    parser.add_argument('url', type=str, help='The starting URL for the web crawler')
    args = parser.parse_args()

    main(args.url)
