from tools import common_tools, scraping_tools
from bs4 import BeautifulSoup


def scrape():
    energy_sources = ('dyzelinas', 'benzinas', 'benzinas/dujos', 'benzinas/elektra', 'elektra', 'dyzelinas/elektra',
                      'dujos', 'benzinas/gamtinės dujos', 'etanolis', 'kitas')
    body_types = ('sendas', 'hečbekas', 'universalas', 'visuregis', 'vienatūris', 'coupe', 'kabrioletas',
                  'keleivinis mikroautobusas', 'kombi mikroautobusas', 'krovininis mikroautobusas',
                  'komercinis auto(su būda)', 'pikapas', 'limuzinas', 'savadarbis auto')

    base_url = 'https://autogidas.lt'
    page_size = 1
    current_page = 1
    prod_url = base_url + '/skelbimai/automobiliai/?f_1[0]=BMW&f_model_14[0]=Serija+3&f_50=kaina_asc&page=' + str(current_page)

    while current_page <= page_size:
        page_html = scraping_tools.scrape_using_crawling_api(prod_url)
        soup = BeautifulSoup(page_html, 'html.parser')

        page_selectors = soup.findAll('div', class_='page')
        for page_selector in page_selectors:
            try:
                if int(scraping_tools.get_element_text(page_selector, 0)) > page_size:
                    page_size = int(scraping_tools.get_element_text(page_selector, 0))
            except ValueError:
                pass

        list_items = soup.find_all('article', class_='list-item')

        for list_item in list_items:
            sold = False
            if list_item.find('div', class_='sold-item') is not None:
                sold = True

            sale_url = base_url + list_item.find('a', class_='item-link')['href']
            title = scraping_tools.get_element_text(list_item.find('h2', class_='item-title'), None)

            if list_item.find('meta', itemprop='price') is not None:
                price = list_item.find('meta', itemprop='price')['content']
            else:
                price = scraping_tools.get_element_text(list_item.find('div', class_='item-price'), 0)

            description_div = list_item.find('div', class_='item-description')
            description = ''
            if description_div is not None:
                description = scraping_tools.get_element_text(description_div.find('h3'), '')
                description += ', ' + scraping_tools.get_element_text(description_div.find('h4'), '')

            description_items = [d.strip() for d in description.split(',')]

            engine_liter = ''
            energy_source = ''
            make_year = ''
            gearbox_type = ''
            power_in_kw = ''
            mileage = ''
            sale_location = ''
            body_type = ''

            for item in description_items:
                if ' l.' in item:
                    engine_liter = common_tools.get_first_number_in_string(item, ' ')
                elif item.lower() in energy_sources:
                    energy_source = item
                elif ' m' in item:
                    make_year = common_tools.get_first_number_in_string(item, ' ')
                elif item.lower() in ('mechaninė', 'automatinė'):
                    gearbox_type = item
                elif ' kW' in item:
                    power_in_kw = common_tools.get_first_number_in_string(item, ' ')
                elif ' km.' in item:
                    mileage = common_tools.get_first_number_in_string(item.replace(" ", "").replace("km.", "").replace("km", ""), ' ')
                elif item.lower() in body_types:
                    body_type = item
                else:
                    sale_location = item

            if make_year is not None:
                make_year = int(make_year)

            print(title, sale_url, sold, price, engine_liter, energy_source, make_year, gearbox_type, power_in_kw, mileage, sale_location, body_type)

        current_page += 1
        prod_url = 'https://autogidas.lt/skelbimai/automobiliai/?f_1[0]=BMW&f_model_14[0]=Serija+3&f_50=kaina_asc&page=' + str(current_page)

        if current_page > page_size:
            break

