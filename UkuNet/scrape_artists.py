# scrapping artists
import requests
import string

from bs4 import BeautifulSoup
from tqdm import tqdm
from UkuNet.utilities import save_json

def get_artists():
    url_dict = {}
    count = 0
    for letter in tqdm(string.ascii_lowercase):
        letter_list = []

        r = requests.get("https://ukutabs.com/{}/".format(letter))
        if r.status_code != 200:
            raise Exception("Wrong Response.")
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        for li in soup.find_all('li', class_='cat-item'):
            for a in li.find_all('a'):
                count += 1
                letter_list.append(a['href'])
        url_dict[letter] = letter_list

    print('Found {} artists'.format(count))
    save_json(url_dict, 'artists')

    return url_dict

if __name__ == '__main__':
    get_artists()
