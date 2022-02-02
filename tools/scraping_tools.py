from proxycrawl import CrawlingAPI
import requests


def scrape(url):
    return requests.get(url).content


def scrape_local(file_path):
    html_file = open(file_path, "r", encoding="utf8")
    return html_file.read()


def scrape_using_crawling_api(url):
    token = ''
    api = CrawlingAPI({'token': token})
    response = api.get(url)
    if response['status_code'] == 200:
        return response['body']
    else:
        print('Failure, status code: ', response['status_code'])
        print('Trying again')
        return scrape_using_crawling_api(url)


def get_element_text(element, null_value):
    try:
        return element.contents[0].strip()
    except:
        return null_value

