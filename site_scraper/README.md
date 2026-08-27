## Target Classification

The site I will be scarping is toscrape.com. It is a fictional bookstore built for the sole purpose of being scrapped for users to learn web scraping.
The first 3 catalogue pages will be scraped. The data collected will be raw text fields. Just collecting raw text fields is enough to practice collecting data from a site.


## toscrape.com robots.txt

After visiting the url: https://books.toscrape.com/robots.txt, not robots.txt file was found (404 Not Found)


## Oath

I will not reuse this code on another site without checking its rules and terms first.


## How to run

First install requirements.txt by doing 'pip install requirements.txt'

Then cd into the src folder and then type 'py main.py' in the terminal


## Record Schema to validate information

The record schema I used to validate all the information was:

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


## Politeness Rules

When sending requests to the website, I created a user-agent so the server knew exactly who was
making the request.
I added a delay of 0.5 between requests and and a timeout of 5 seconds for the request.
I also made sure to cache the data so no unnecessary calls would be made.


## run-report.json output
Below is an example report run:
{
  "start_time": "2026-08-27 05:01:36.140008+00:00",
  "duration": 0.382077,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}

No browser was necessary for this web scraper as the data was already in html that the server gives us


## Ethics

This project scraper should use an official API when one is available. This project must never bypass logins, paywalls, or blocks. You should collect only what you need.