import time
import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

TARGET='Remi Yuan'
COUNTRY_WHITELIST = []

def get_proxies_by_country(country):
    proxies = requests.get('https://www.proxy-list.download/api/v1/get', params={'type': 'http', 'country': country}).text
    proxies = proxies.split('\r\n')

    return [('', "http://{}".format(p)) for p in proxies]

class ProxySession(object):
    def __init__(self, proxy_manager):
        self.manager = proxy_manager
        self.proxy = self.manager.new_proxies.pop()

    def __enter__(self):
        session = requests.session()
        print "{} - {}".format(*self.proxy)

        session.headers = session.headers.update(self.manager.headers)

        session.proxies = {}
        session.proxies['http'] = self.proxy[1]
        session.proxies['https'] = self.proxy[1]

        return session

    def __exit__(self, *args):
        self.manager.used_proxies.add(self.proxy)

class ProxyManager(object):
    def __init__(self, headers={}):
        self.headers = headers
        self.used_proxies = set([])
        self.new_proxies = get_proxies_by_country('CA') + get_proxies_by_country('US')

    def new_session(self):
        if len(self.new_proxies) < 1:
            print "Fetching new proxies"
            self.new_proxies = self.fetch_new_proxies()

        return ProxySession(self)

if __name__ == '__main__':
    proxy = ProxyManager(headers= {'User-Agent': 'Mozilla/5.0'})
    def attempt_vote(*args):
        with proxy.new_session() as session:
            time.sleep(10)
            try:
                res = session.get('http://httpbin.org/ip', timeout=20)
                res = res.json()
                if 'origin' not in res:
                    raise
                res = session.get('http://www.arthere.ca/vote', timeout=20)
                res = BeautifulSoup(res.content, features='html5lib')

                target = res.findAll('div', {'class': 'name'}, text=TARGET)[0]
                target = target.parent.find('a', {'class': 'plus1-link'})
                target = 'http://www.arthere.ca' + target.attrs['href']

                res = session.get(str(target), timeout=20)
                if res.ok:
                    print 'Sucessful Vote! {}'.format(num_votes + 1)
                    num_votes +=1
            except:
                pass

    pool = ThreadPool(processes=20)
    pool.map(attempt_vote, range(1000))
