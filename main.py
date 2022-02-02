from scrapers import autoplius_scraper
from scrapers import autogidas_scraper
from scrapers import brc_scraper
from scrapers import longo_scraper


if __name__ == '__main__':
    brc_scraper.scrape()
    longo_scraper.scrape()
    autogidas_scraper.scrape()
    autoplius_scraper.scrape()

