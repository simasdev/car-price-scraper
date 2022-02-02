from tools import common_tools, scraping_tools
from bs4 import BeautifulSoup


def scrape():
    page_size = 1
    current_page = 1
    base_url = 'https://longo.lt'
    prod_url = 'https://longo.lt/katalogas?makes=BMW&search=&orderBy=RECOMMENDED&gridMode=GRID&multiSelect=true&pageSize=4000&currentPage=' + str(current_page)

    while current_page <= page_size:
        page_html = scraping_tools.scrape(prod_url)
        soup = BeautifulSoup(page_html, 'html.parser')

        page_selectors = soup.find_all('button', class_='page-link')
        for page_selector in page_selectors:
            try:
                if int(scraping_tools.get_element_text(page_selector, 0)) > page_size:
                    page_size = int(scraping_tools.get_element_text(page_selector, 0))
            except ValueError:
                pass

        cars = soup.find_all('a', class_='v-card-item')
        for car in cars:

            if 'v-card-item--reserved' in car['class']:
                sold = True

            sale_url = car['href']

            content_div = car.find('div', class_='v-card-item__content')

            title = " ".join((scraping_tools.get_element_text(content_div.find('div', class_='v-card-item__title'), '').replace('\n', '').split()))

            price = scraping_tools.get_element_text(car.find('div', class_='v-card-item__full-price').find('span', class_='v-card-item__price-value'), None)

            if price is not None:
                price = common_tools.get_first_number_in_string(price.replace(" ", "").replace("€", ""), ' ')

            make_year = int(common_tools.get_first_number_in_string(title, ' '))

            car_details = car.find('div', class_='v-card-item__details').findAll('div', class_='chip')

            mileage = int(scraping_tools.get_element_text(car_details[0], '').replace('km', '').replace(' ', ''))
            energy_source = scraping_tools.get_element_text(car_details[1], '')
            gearbox_type = scraping_tools.get_element_text(car_details[2], '')

            print(title, base_url + sale_url, price, make_year, mileage, energy_source, gearbox_type)

        current_page += 1
        prod_url = 'https://longo.lt/katalogas?makes=BMW&search=&orderBy=RECOMMENDED&gridMode=GRID&multiSelect=true&pageSize=4000&currentPage=' + str(current_page)

        if current_page > page_size:
            break

