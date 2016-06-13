# coding: utf-8

import logging
logging.getLogger().setLevel(logging.INFO)


import os
import re
from collections import namedtuple

import requests
from lxml import html

class Album(namedtuple('Album', 'title cover publish_date song_ids')):

    @property
    def album_home(self):
        return 'data/%s' % self.title

    def fetch(self, with_songs=False):
        if not os.path.exists(self.album_home):
            os.makedirs(self.album_home)

        res = requests.get(self.cover, stream=True)
        with open('%s/cover.jpg' % self.album_home, 'wb') as fd:
            for chunk in res.iter_content(128):
                fd.write(chunk)
        if with_songs:
            for song_id in self.song_ids:
                song = get_song_info(song_id)
                song.fetch(self.album_home)

class Song(namedtuple('Song', 'id title writer composer')):

    @property
    def svg_url(self):
        return 'http://www.uta-net.com/user/phplib/svg/showkasi.php?ID=%s' % self.id

    @property
    def filename(self):
        return '%s_%s_%s.svg' % (self.title, self.writer, self.composer)

    def fetch(self, path):
        res = requests.get(self.svg_url, stream=True)
        with open('%s/%s' % (path, self.filename), 'wb') as fd:
            for chunk in res.iter_content(128):
                fd.write(chunk)
        logging.info('[Song]%s done!' % self.title)

UTA_NET = 'http://www.uta-net.com'
ALBUM_INDEX_URL = 'http://www.uta-net.com/user/search_index/artist.html?AID=3024'

def get_song_info(song_id):
    song_url = 'http://www.uta-net.com/song/%s/' % song_id
    title_xpath = '//*[@id="view_kashi"]/div[1]/h2'
    writer_composer_xpath = '//*[@id="view_kashi"]/div[2]/div[2]/h4'

    song_page = requests.get(song_url)
    song_page_root = html.fromstring(song_page.content)

    title =song_page_root.xpath(title_xpath)[0].text
    writer, composer = map(lambda e: e.text, song_page_root.xpath(writer_composer_xpath))
    return Song(song_id, title, writer, composer)

def get_album_info(album_el):
    cover_xpath = './/*[@class="album_image"]/a/img'
    publish_xpath= './/*[@class="album_title"]/dl/dd[1]'
    links_xpath = './/*[@class="album_songs"]/li/a'

    cover = UTA_NET + album_el.xpath(cover_xpath)[0].get('src')
    title = album_el.xpath(cover_xpath)[0].get('alt')
    publish_date = album_el.xpath(publish_xpath)[0].text
    links = album_el.xpath(links_xpath)
    song_ids = map(lambda e: re.findall(r'/song/(.+?)/', e.get('href'))[0], links)
    return Album(title, cover, publish_date, song_ids)


def get_all_album_els():
    res = requests.get(ALBUM_INDEX_URL)
    root = html.fromstring(res.content)
    return root.xpath('//*[@id="album_contents"]/div[2]/div[1]/div[2]/table')

def main():
    album_els = get_all_album_els()
    for album_el in album_els:
        album = get_album_info(album_el)
        album.fetch(with_songs=True)
        logging.info('[Album]%s done!' % album.title)


if __name__ == '__main__':
    main()
