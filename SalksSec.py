import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import os
from colorama import Fore, Style, init
import time

# Inicializar colorama
init(autoreset=True)

# Função para imprimir a arte ASCII com gradiente
def print_ascii_art():
    ascii_art = """                                                             
 (`-').->                  <-.(`-')  
 ( OO)_              <-.    __( OO)  
(_)--\_)    .---.  ,--. )  '-'. ,--. 
/    _ /   / .  |  |  (`-')|  .'   / 
\_..`--.  / /|  |  |  |OO )|      /) 
.-._)   \/ '-'  ||(|  '__ ||  .   '  
\       /`---|  |' |     |'|  |\   \ 
 `-----'     `--'  `-----' `--' '--'                                   
      + the Salk's multitool  +                  
"""
    colors = [Fore.LIGHTBLUE_EX, Fore.BLUE]
    for line in ascii_art.splitlines():
        for i, char in enumerate(line):
            gradient = colors[i % len(colors)]
            print(gradient + char, end="")
        print("")
        time.sleep(0.1)

# Web Crawler Functionality
def web_crawler(start_url):
    def get_links(html, base_url):
        links = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tags = soup.find_all('a')
            for tag in tags:
                link = tag.get('href')
                if link:
                    absolute_link = urljoin(base_url, link)
                    links.append(absolute_link)
        except Exception as e:
            print(f"Error while parsing HTML: {e}")
        return links

    to_crawl = [start_url]
    crawled = set()

    while to_crawl:
        url = to_crawl.pop(0)
        if url in crawled:
            continue

        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            links = get_links(html, url)

            for link in links:
                if link not in crawled and link not in to_crawl:
                    to_crawl.append(link)

            print(f'Crawling {url}')
            crawled.add(url)

        except requests.exceptions.RequestException as e:
            print(f"Failed to crawl {url}: {e}")

    if not to_crawl:
        print('No more links to crawl.')

# Email Crawler Functionality
def email_crawler(file_path):
    import re

    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        content = file.read()
        emails = re.findall(email_pattern, content)

    if emails:
        print("Emails found:")
        for email in set(emails):
            print(email)
    else:
        print("No emails found.")

# Directory Brute-Force Functionality
def dir_brute_force(url, wordlist):
    if not os.path.isfile(wordlist):
        print(f"The wordlist file {wordlist} does not exist.")
        return

    with open(wordlist, 'r') as file:
        paths = file.read().splitlines()

    for path in paths:
        full_url = urljoin(url, path)
        try:
            response = requests.head(full_url)
            if response.status_code == 200:
                print(f"Found: {full_url}")
        except requests.exceptions.RequestException:
            pass

# Main menu and argument handling
def main():
    print_ascii_art()

    parser = argparse.ArgumentParser(
        description="S4lk's Secret - Multitool for Web Crawling, Email Crawling, and Directory Brute-forcing"
    )
    parser.add_argument('-wc', '--webcrawler', type=str, help='Start URL for web crawler')
    parser.add_argument('-ec', '--emailcrawler', type=str, help='File path for email crawler')
    parser.add_argument('-db', '--dirbruteforce', nargs=2, metavar=('URL', 'WORDLIST'),
                        help='URL and wordlist for directory brute-force')
    parser.add_argument('-help', action='store_true', help='Display help menu')
    args = parser.parse_args()

    if args.help:
        print("\n=== HELP MENU ===")
        print("-wc, --webcrawler    : Start URL for web crawler")
        print("-ec, --emailcrawler  : File path for email crawler")
        print("-db, --dirbruteforce : URL and wordlist for directory brute-force")
        print("-help                : Display this help menu\n")
        return

    if args.webcrawler:
        print(f"Starting Web Crawler on {args.webcrawler}")
        web_crawler(args.webcrawler)

    if args.emailcrawler:
        print(f"Starting Email Crawler on {args.emailcrawler}")
        email_crawler(args.emailcrawler)

    if args.dirbruteforce:
        url, wordlist = args.dirbruteforce
        print(f"Starting Directory Brute-Force on {url} with wordlist {wordlist}")
        dir_brute_force(url, wordlist)

    if not any(vars(args).values()):
        print("Please provide valid arguments. Use -help for assistance.")

if __name__ == "__main__":
    main()
