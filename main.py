import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(long_url, token):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization':token}
    payload = {'long_url':long_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    response = response.json()
    bitlink = response.get('link')
    return bitlink


def count_clicks(bitlink, token):
    bitlink = urlparse(bitlink)
    bitlink = f'{bitlink.netloc}{bitlink.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    payload = {'Authorization': token}
    response = requests.get(url, headers=payload)
    response.raise_for_status()
    response = response.json()
    total_clicks = response.get('total_clicks')
    return total_clicks
  

def check_url(url, token):
    url = urlparse(url)
    url = f'{url.netloc}{url.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    payload = {'Authorization': token}
    response = requests.get(url, headers=payload)
    return response.ok


def main():
    load_dotenv()
    bitler = argparse.ArgumentParser(description = 'Укорчаиваем ссылку, или считаем клики')
    bitler.add_argument('url', help='Ссылка')
    args = bitler.parse_args()
    url = args.url
    if '//' not in url:
        url = '%s%s' % ('http://', url)
    bitly_token = f'Bearer {os.getenv("BITLY_TOKEN")}'
    checked_url = check_url(url, bitly_token)
    try:
        if checked_url:
            print('Число переходов по ссылке за все время: ', count_clicks(url, bitly_token))
        else:
            print('Битлинк:', shorten_link(url, bitly_token))
    except requests.exceptions.HTTPError as error:
            exit('Ошибка при вводе адреса:\n{0}'.format(error))


if __name__ == '__main__':
    main()