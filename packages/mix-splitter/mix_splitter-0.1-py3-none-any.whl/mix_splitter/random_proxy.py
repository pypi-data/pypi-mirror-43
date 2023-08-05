from bs4 import BeautifulSoup
import requests
import random


def random_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    proxy_formatted = format_proxy(proxy)

    return proxy_formatted


def format_proxy(proxy):
    proxy_format = 'http://{}:{}'
    formatted = proxy_format.format(proxy['ip'], proxy['port'])

    return formatted


def delete_proxy(proxy_list, proxy):
    proxy_list.remove(proxy)


def get_proxy_list():
    proxy_list = []

    proxies_req = requests.get(
        'https://www.sslproxies.org',
    )

    page = proxies_req.text
    page_parsed = BeautifulSoup(page, features='lxml')
    proxies_table = page_parsed.find(id='proxylisttable')
    proxy_rows = proxies_table.tbody.find_all('tr')

    for row in proxy_rows:
        proxy_list.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    return proxy_list


proxy_list = get_proxy_list()


def main():
    proxy = random_proxy(proxy_list)

    return proxy


if __name__ == '__main__':
    main()
