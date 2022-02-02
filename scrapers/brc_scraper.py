from tools import common_tools, scraping_tools
from bs4 import BeautifulSoup


def scrape():
    page_size = 1
    current_page = 1
    prod_url = 'https://lt.brcauto.eu/automobiliu-paieska?makes=2104&per_page=10000&search=1&page=' + str(current_page)

    while current_page <= page_size:
        page_html = scraping_tools.scrape(prod_url)
        soup = BeautifulSoup(page_html, 'html.parser')

        page_selectors = soup.find_all('a', class_='page-link')
        for page_selector in page_selectors:
            try:
                if int(scraping_tools.get_element_text(page_selector, 0)) > page_size:
                    page_size = int(scraping_tools.get_element_text(page_selector, 0))
            except ValueError:
                pass

        cars = soup.find_all('div', class_='cars')
        for car in cars:
            sold = False

            sale_url = car.find('h2', class_='cars__title').find('a')['href']
            title = scraping_tools.get_element_text(car.find('h2', class_='cars__title').find('a'), None)
            price = scraping_tools.get_element_text(car.find('div', class_='cars-price'), None)

            description = scraping_tools.get_element_text(car.find('p', class_='cars__subtitle'), '')
            description_parts = [d.strip() for d in description.split('|')]

            make_year = int(common_tools.get_first_number_in_string(description_parts[0], ' '))
            energy_source = ''.join([c for c in description_parts[1] if not c.isdigit() and c != '.'])
            gearbox_type = description_parts[2]
            mileage = common_tools.get_first_number_in_string(description_parts[3], ' ')
            power_in_kw = common_tools.get_first_number_in_string(description_parts[4], ' ')
            color = description_parts[5]

            price = common_tools.get_first_number_in_string(price.replace(" ", "").replace("€", ""), ' ')

            print(title, sale_url, price, make_year, energy_source, gearbox_type, mileage, power_in_kw, color)

        current_page += 1
        prod_url = 'https://lt.brcauto.eu/automobiliu-paieska?makes=2104&per_page=10000&search=1&page=' + str(current_page)

        if current_page > page_size:
            break

