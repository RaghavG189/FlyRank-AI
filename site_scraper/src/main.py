#Import libraries for web scraping
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests




#Store url to be scraped
url = "https://books.toscrape.com/catalogue/page-1.html"

#Store path where HTML will be saved
file_path = Path("cache/catalogue-page-1.html")

#Define user agent
repo_link = "https://github.com/RaghavG189/FlyRank-AI/tree/main/site_scrapper"
headers = {"user_agent": f"FlyRankInternship-A5/1.0+{repo_link}"}

#List used to store all book urls
book_urls = []


#Function will check if .html file is present and if not will make a request to the site and save the data
def save_data(file_path):

    if not file_path.is_file():
        try:

            #Use requests to get HTML content from page
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

        except requests.exceptions.HTTPError as error: #If server throws error then raise the error

            print(f"An HTTP error occurred: {error}")


        print("FETCH")

        #Save the HTML file in cache/
        with open(file_path,'w', encoding='utf-8') as f:

            f.write(response.text)

        print(len(response.content))
        
    else:
        #.html file is already present in cache/
        print("CACHE HIT")
        print(len(file_path.read_bytes()))


#Retrieves all links from h3 tags and combines with the url
def store_links(soup, url_list):

    for link in soup.select('h3 a'):
        href = link.get('href') #Get book link

        abs_link = urljoin(url, href) #Merge book link with url

        url_list.append(abs_link) #Appends the absolute url to a list


#Returns soup object given file_path
def get_soup(file_path):

    with open(file_path) as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup



for i in range(3):

    save_data(file_path)

    soup = get_soup(file_path)

    store_links(soup, book_urls)

    next_button = soup.find("li", class_="next") #Retrieves the line containing the link to the next page
    next_link = next_button.find('a')['href'] #Gets link

    url = urljoin(url, next_link) #Gets new url to get data from

    link_name = Path(next_link).name #Gets the link name
    file_path = Path(f"cache/catalogue-{link_name}") #Gets new file_path to store data
        

print(f"Catalogue_Pages={i+1}, Discovered={len(book_urls)}, unique_urls={len(set(book_urls))}")