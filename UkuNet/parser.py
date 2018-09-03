# parser object to parse one song
from html.parser import HTMLParser
import pandas as pd
from bs4 import BeautifulSoup

def get_genre(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    genre = []

    for div in soup.find_all('div', class_='tagsheader'):
        for tag in div.children:
            if tag.name == 'a':
                genre.append(str(tag.string))

    return genre

class MyHTMLParser(HTMLParser):
    def __init__(self, artist, song, genre):
        HTMLParser.__init__(self)
        self.recording = False
        self.current_tag = []

        self.chords = []
        self.chords_line = []
        self.chords_part = []
        self.lyrics = []
        self.lyrics_part = []
        self.song = song
        self.artist = artist
        self.genre = genre
        self.parts = []


    def handle_starttag(self, tag, attrs):
        self.current_tag.append(tag)
        if tag == 'pre':
            self.recording = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.recording = False
            self.handle_last_batch()
        self.current_tag.pop()


    def handle_data(self, data):
        if self.recording:
            if self.current_tag[-1] == 'strong':
                # a new part of song
                if self.current_tag[-2] == 'strong':
                    # chords may be nested in <strong>
                    whole_name = ''.join([self.parts.pop(), data])
                    self.parts.append(whole_name)
                else:
                    self.parts.append(data)

                if len(self.lyrics_part) != 0 or len(self.chords_part) != 0:
                    # append if not the first part
                    self.lyrics.append(self.lyrics_part[:])
                    self.chords.append(self.chords_part[:])
                    self.lyrics_part.clear()
                    self.chords_part.clear()
            if self.current_tag[-1] == 'a' and data.strip() != '':
                # a new chord
                self.chords_line.append(data)
            if self.current_tag[-1] == 'pre' and data.strip() != '':
                # one line of music finished
                # clean data
                words = data.split()
                lyrics = ' '.join(words)
                if lyrics != '' and lyrics != ':':
                    self.lyrics_part.append(lyrics)
                if len(self.chords_line) != 0:
                    self.chords_part.append(self.chords_line[:])
                    self.chords_line.clear()

    def handle_last_batch(self):
        self.lyrics.append(self.lyrics_part)
        self.chords.append(self.chords_part)

    def dump(self):
        #print(len(self.chords), len(self.parts), len(self.lyrics))
        '''
        try:
            assert(len(self.chords) == len(self.parts))
        except AssertionError:
            print(len(self.chords), len(self.parts))
            print(self.chords)
            print(self.parts)
            raise Exception('AssertionError')

        try:
            assert(len(self.lyrics) == len(self.parts))
        except AssertionError:
            print(len(self.lyrics), len(self.parts))
            print(self.lyrics)
            print(self.parts)
            raise Exception('AssertionError')
        '''

        return {'song': self.song, 'artist': self.artist, 'genre': self.genre, 'chords': self.chords, 'lyrics': self.lyrics, 'parts': self.parts}
