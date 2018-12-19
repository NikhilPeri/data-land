import requests
import bs4
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging

worker=ThreadPoolExecutor(max_workers=20)
TIMEOUT=30
requests.adapters.DEFAULT_RETRIES = 3
ROOT_URL='https://www.kijiji.ca' # This should be done better

def scrape_ad(ad):
    ad_url = ROOT_URL + ad.find('a').attrs['href']
    ad = bs4.BeautifulSoup(requests.get(ad_url, timeout=TIMEOUT).text)

    attribute_list = ad.find(id='AttributeList').find_all('li')
    attributes = {}
    for a in attribute_list:
        a = a.find('dd')
        if a is None:
            continue
        if 'itemprop' in a.attrs:
            attributes[a.attrs['itemprop'] ] = a.contents[0]

    return {
        'url':          ad_url,
        'price':        ad.find(itemprop='price').text,
        'date':         ad.find(itemprop='datePosted').find('time').attrs['datetime'],
        'location':     ad.find(itemprop='address').text,
        'title':        ad.find('h1', itemprop='name').text,
        'description':  ad.find(itemprop='description').text,
        'attributes':   attributes,
    }

def safe_scrape_ad(ad):
    try:
        return scrape_ad(ad)
    except Exception as e:
        ad_url = ROOT_URL + ad.find('a').attrs['href']
        logging.error('AD: {} Exception: {}'.format(ad_url, e))

def scrape_page(page):
    ads = page.find_all('div', 'regular-ad')
    ads = worker.map(safe_scrape_ad, ads)
    return list(ads)

if __name__ == '__main__':
    import sys
    import json
    import time
    output_file = sys.argv[1]
    page_url = sys.argv[2]

    if not page_url.startswith(ROOT_URL):
        raise AttributeError('page url must begin with {}'.format(ROOT_URL))

    output_file = open(output_file, 'w+')
    output_file.write('[')
    ad_counter=0
    while page_url is not None:
        try:
            page = bs4.BeautifulSoup(requests.get(page_url, timeout=TIMEOUT).text)
            ads = [output_file.write(json.dumps(ad, indent=2) + ',') for ad in scrape_page(page)]
            ad_counter +=len(ads)
            print('Fetched {} ads'.format(ad_counter))
            next_page=page.find('span', title='Next')
            if next_page is not None:
                page_url = ROOT_URL + next_page.attrs['data-href']
            else:
                page_url = None
        except Exception as e:
            logging.error(e)

    output_file.write(']')
    output_file.close()
