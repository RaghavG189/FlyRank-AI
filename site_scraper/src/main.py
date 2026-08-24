#Import libraries for web scraping
from bs4 import BeautifulSoup
import requests




#Get url to be scraped
url = "https://books.toscrape.com/catalogue/page-1.html"


#Define user agent
repo_link = "https://github.com/RaghavG189/FlyRank-AI/tree/main/site_scrapper"
headers = {"user_agent": f"FlyRankInternship-A5/1.0+{repo_link}"}


try:

    #Use requests to get HTML content from page
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()

except requests.exceptions.HTTPError as error:

    print(f"An HTTP error occurred: {error}")


with open('cache/catalogue-page-1.html', 'w') as f:

    f.write(response.text)

