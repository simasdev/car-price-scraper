from tools import common_tools, scraping_tools
from bs4 import BeautifulSoup


def scrape():
    page_size = 1
    current_page = 1
    prod_url = 'https://autoplius.lt/skelbimai/naudoti-automobiliai?make_id=97&model_id=1319&page_nr=' + str(current_page)

    while current_page <= page_size:
        page_html = scraping_tools.scrape_using_crawling_api(prod_url)
        soup = BeautifulSoup(page_html, 'html.parser')

        page_selectors = soup.find('div', class_='page-navigation-container').find_all('span')

        for page_selector in page_selectors:
            try:
                if int(scraping_tools.get_element_text(page_selector, 0)) > page_size:
                    page_size = int(scraping_tools.get_element_text(page_selector, 0))
            except ValueError:
                pass

        announcement_items = soup.find_all('a', class_='announcement-item')
        for announcement_item in announcement_items:
            sold = False
            if 'is-sold' in announcement_item['class']:
                sold = True

            sale_url = announcement_item['href']
            title = scraping_tools.get_element_text(announcement_item.find('div', class_='announcement-title'), None)
            price = scraping_tools.get_element_text(announcement_item.find('div', class_='announcement-pricing-info').find('strong'), None)
            make_year = scraping_tools.get_element_text(announcement_item.find('span', title='Pagaminimo data'), None)
            energy_source = scraping_tools.get_element_text(announcement_item.find('span', title='Kuro tipas'), None)
            gearbox_type = scraping_tools.get_element_text(announcement_item.find('span', title='Pavarų dėžė'), None)
            power_in_kw = scraping_tools.get_element_text(announcement_item.find('span', title='Galia'), None)
            mileage = scraping_tools.get_element_text(announcement_item.find('span', title='Rida'), None)
            sale_location = scraping_tools.get_element_text(announcement_item.find('span', title='Miestas'), None)
            body_type = scraping_tools.get_element_text(announcement_item.find('span', title='Kėbulo tipas'), None)

            price = common_tools.get_first_number_in_string(price.replace(" ", "").replace("€", ""), ' ')

            if power_in_kw is not None:
                power_in_kw = common_tools.get_first_number_in_string(power_in_kw.replace(" ", "").replace("kW", ""), ' ')

            if mileage is not None:
                mileage = common_tools.get_first_number_in_string(mileage.replace(" ", "").replace("km", ""), ' ')

            print(title, sale_url, price, make_year, energy_source, gearbox_type, power_in_kw, mileage, sale_location, body_type)

        current_page += 1
        prod_url = 'https://autoplius.lt/skelbimai/naudoti-automobiliai?make_id=97&model_id=1319&page_nr=' + str(current_page)

        if current_page > page_size:
            break

