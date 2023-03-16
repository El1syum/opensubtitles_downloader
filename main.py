import os
import string
import time

import requests
from bs4 import BeautifulSoup
import logging

if not os.path.exists('logs/'):
    os.mkdir('logs')

logging.basicConfig(filename='logs/bot.log', level=logging.INFO, encoding='utf-8')


def get_data():
    if not os.path.exists('subtitles'):
        os.mkdir('subtitles')

    off = 0
    str = string.ascii_lowercase + '#'

    for c in str:

        url = f'https://www.opensubtitles.org/en/search/sublanguageid-all/moviename-{c}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        count = round(int(
            soup.find('div', id='msg').find('span', style='float:right;').text.split('of')[1].split('(')[0]) / 40) + 1

        while True:
            url = f'https://www.opensubtitles.org/en/search/sublanguageid-all/moviename-{c}/offset-{off}'
            off += 40
            if off > count * 40:
                break

            logging.info(url)

            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            cards = soup.find_all('tr', class_='change')

            for card in cards[:10]:
                url = 'https://www.opensubtitles.org' + card.find('a').get('href')
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'lxml')

                link = 'https://www.opensubtitles.org' + soup.find('a', id='bt-dwl-bt').get('href')
                filename = soup.find('a', id='bt-dwl-bt').get('data-installer-file-name')
                if os.path.exists(f'subtitles/{filename}.zip'):
                    continue

                response = requests.get(url=link)
                with open(f'subtitles/{filename}.zip', 'wb') as file:
                    file.write(response.content)

                logging.info(f'{filename} saved successfully!')

                time.sleep(1)

            break
        break


if __name__ == '__main__':
    get_data()
