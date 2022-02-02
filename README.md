# Car price scraper

A simple scraper, that gets data from main used cars marketplaces in Lithuania:

- https://www.autoplius.lt
- https://www.autogidas.lt
- https://www.lt.brcauto.eu
- https://www.longo.lt

This scraper is configured to get data only about BMW brand cars.

Scraper does not go into each sale url and collects data from sale preview - this helps to
minimize requests amount.
## Usage/Examples


At the time of creating this, autogidas.lt and autoplius.lt have some level of protection against
scraping that can be bypassed using Selenium, however, I chose to use third party API to do this
(proxycrawl.com) since I had some free credits. You need to enter your proxycrawl token value to
tools/scraping_tools.py proxycrawl_token variable.

In order to run the scraper, just run main.py file and it will print the results to the console.
