# scraping songs
import requests
import string

from bs4 import BeautifulSoup
from tqdm import tqdm
from UkuNet.utilities import save_json, load_json

def get_songs():
    artists = load_json('artists')
    songs = {}
    count = 0

    for letter, l in tqdm(artists.items()):
        for url in l:
            artist_name = url.split('/')[-2]
            songs_list = []

            r = requests.get(url)
            if r.status_code != 200:
                raise Exception("Wrong Response.")
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')

            for ul in soup.find_all('ul', class_='archivelist'):
                for li in ul.children:
                    songs_list.append(li.a['href'])
                    count += 1

            songs[artist_name] = songs_list

    print("Found {} songs.".format(count))
    save_json(songs, 'songs')

    return songs
