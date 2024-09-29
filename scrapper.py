from bs4 import BeautifulSoup
import requests
import re

class Scraper():
    def __init__(self) -> None:
        pass
    def scraper(self, link): 
        url = link
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        containers = soup.find_all("div", class_="container")
        href_links = []
        for container in containers:
            a_tags = container.find_all("a", class_="inv", href=True)
        for a_tag in a_tags:
            href_links.append(a_tag['href'])
        return href_links

    def name_from_links(self, list):
        topics = []
        for url in list:
            pattern = r"chapter/([^/]+)/"
            match = re.search(pattern, url)
            if match:
                module_name = match.group(1).replace("-", " ").title()
                topics.append(module_name)
        return(topics)

# print(name_from_links(scraper("https://zerodha.com/varsity/module/sector-analysis/")))

