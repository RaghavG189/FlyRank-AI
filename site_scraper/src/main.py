#Import libraries for web scraping
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel, ValidationError



#Store url to be scraped
page_url = "https://books.toscrape.com/catalogue/page-1.html"

#Store path where HTML will be saved
file_path_catalogue = Path("cache/catalogue-page-1.html")

#Define user agent
repo_link = "https://github.com/RaghavG189/FlyRank-AI/tree/main/site_scrapper"
headers = {"user-agent": f"FlyRankInternship-A5/1.0+{repo_link}"}

#List used to store page url and book url as a tuple
book_urls = []

#List used to store book metadata as dicts
book_records = []



#Function will check if .html file is present and if not will make a request to the site and save the data
def save_data(file_path, url):

    if not file_path.is_file():
        try:

            #Use requests to get HTML content from page
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            print("FETCH")

            time.sleep(0.5)

            #Save the HTML file in cache/
            with open(file_path,'w', encoding='utf-8') as f:

                f.write(response.content.decode("utf-8"))

            print(len(response.content))

            response = "FETCH"            

        except requests.exceptions.HTTPError as error: #If server throws error then raise the error

            print(f"An HTTP error occurred: {error}")
            return error
            

    else:
        #.html file is already present in cache/
        print("CACHE HIT")
        print(len(file_path.read_bytes()))

        response = "CACHE HIT"


    return response


#Retrieves all links from h3 tags and combines with the url
def store_links(soup, book_url_list, url):

    for link in soup.select('h3 a'):
        href = link.get('href') #Get book link

        abs_link = urljoin(url, href) #Merge book link with url

        tuple_data = (url, abs_link)

        book_url_list.append(tuple_data) #Appends the tuple to a list


#Retrieves all book metadata and stores it in a dict
def store_book_data(soup, book_dicts, book_tuple, fetched_time):

    #unpack the tuple
    source_url, book_url = book_tuple

    title_element = soup.find("h1")
    title = title_element.get_text(strip=True) if title_element else None

    product_url = book_url

    price_element = soup.find("p", class_="price_color")
    price_text =  price_element.get_text(strip=True) if price_element else None

    availability_element = soup.find("p", class_="instock availability")
    availability_text = availability_element.get_text(strip=True) if availability_element else None

    rating_element = soup.select_one("p.star-rating")
    rating_text = rating_element.get("class", [])
    rating = rating_text[-1] 

    description_header = soup.find("div", id="product_description")
    description_element = description_header.find_next_sibling("p")
    description = description_element.get_text(strip=True) if description_element else None

    source_page = source_url

    fetched_at = fetched_time

    metadata = {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }

    book_dicts.append(metadata)
   

#Returns new url and filepath for catalogue pages
def get_page(soup, url):

    next_button = soup.find("li", class_="next") #Retrieves the line containing the link to the next page
    next_link = next_button.find('a')['href'] #Gets link
    
    url = urljoin(url, next_link) #Gets new url to get data from
    
    link_name = Path(next_link).name #Gets the link name
    file_path = Path(f"cache/catalogue-{link_name}") #Gets new file_path to store data

    return url, file_path


#Returns soup object given file_path
def get_soup(file_path):

    with open(file_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    return soup



#Stage 2 stash urls for 3 catalogue pages
for i in range(3):

    response = save_data(file_path_catalogue, page_url)

    #Temporary error handling - no way to get next link if cant get current page data
    if isinstance(response, requests.exceptions.HTTPError):
        print(f"Data from page {i+1} could not be retrieved. Stopping data scraping.")
        break

    soup = get_soup(file_path_catalogue)

    store_links(soup, book_urls, page_url) #Stores abs_links for a catalogue in book_urls

    page_url, file_path_catalogue = get_page(soup, page_url) #Gets new url and file_path for next catalogue

unique_urls = set(book_urls) #Get rid of any duplicates
print(f"catalogue_pages={i+1}, discovered={len(book_urls)}, unique_urls={len(unique_urls)}")




#Stage 3 stage book metadata for every url in list
for unique_url in unique_urls:

    source_url, book_url = unique_url

    #Extract name from link to create file_path_book
    book_name = Path(book_url).parent.name #REVISIT: See if we could do something similar for the catalogue file paths
    file_path_book = Path(f"cache/book-{book_name}.html")

    #Get data for every book and save it as .html
    response = save_data(file_path_book, book_url)

    if isinstance(response, requests.exceptions.HTTPError): #Temporary error handling - we already have all the urls so skip to next one

        continue

    if response == "FETCH":

        fetched_time = datetime.now(timezone.utc)
        fetched_time = fetched_time.strftime('%Y-%m-%dT%H:%M:%S')

    elif response == "CACHE HIT":

        fetched_time = file_path_book.stat().st_birthtime
        fetched_time = datetime.fromtimestamp(fetched_time).strftime('%Y-%m-%dT%H:%M:%S')

    #Get soup
    soup = get_soup(file_path_book)

    #Stores metadata for a book in a list
    store_book_data(soup, book_records, unique_url, fetched_time)
print(f"Complete record: {book_records[0]}, detail_pages: {len(book_records)}")


#Stage 4 - clean, check, store

class record_schema(BaseModel):

    title: str
    product_url: str
    price_text: str
    availability_text: str
    rating_text: str
    description: str | None
    source_page: str
    fetched_at: str
    price_gbp: float


verified_records = []
error_records = []

for book_record in book_records:


    try:
        price = book_record["price_text"].replace("£", "")
        book_record["price_gbp"] = float(price)
    except ValueError as e:

        bad_record = {
            "record": book_record,
            "reason": "Invalid Price Format"
        }

        error_records.append(bad_record)
        continue


    try:
        verification = record_schema(title=book_record.get("title"), product_url=book_record.get("product_url"),
                                    price_text=book_record.get("price_text"), availability_text=book_record.get("availability_text"),
                                    rating_text=book_record.get("rating_text"), description=book_record.get("description"),
                                    source_page=book_record.get("source_page"), fetched_at=book_record.get("fetched_at"),
                                    price_gbp=book_record.get("price_gbp")
                                    )
        
        verification = verification.model_dump_json() #Make it json serializable
        verified_records.append(verification)

    except ValidationError as e:

        bad_record = {
           "record": book_record,
           "reason": e.errors() 
        }

        error_records.append(bad_record)


#Save good records
with open("output/books.json", "w", encoding="utf-8") as f:

    json.dump(verified_records, f, indent=2)


#Save bad records
with open("errors.json", "w", encoding="utf-8") as f:

    json.dump(error_records, f, indent=2)


    
