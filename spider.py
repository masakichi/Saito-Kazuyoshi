# coding: utf-8

import re
from collections import namedtuple

import requests
from lxml import html, etree

Album = namedtuple('Album', 'title cover publish_date song_ids')

UTA_NET = 'http://www.uta-net.com'
ALBUM_INDEX_URL = 'http://www.uta-net.com/user/search_index/artist.html?AID=3024'

def get_svg(song_id):
    svg_url = 'http://www.uta-net.com/user/phplib/svg/showkasi.php?ID=%s' % song_id
    res = requests.get(svg_url, stream=True)
    with open('/tmp/test/%s.svg' % song_id, 'wb') as fd:
        for chunk in res.iter_content(128):
            fd.write(chunk)

def get_album_info(album_el):
    cover_xpath = '//*/tr[2]/td[1]/div[1]/a/img'
    title_xpath = '//*/tr[2]/td[1]/div[2]/p'
    publish_xpath= '//*/tr[2]/td[1]/div[2]/dl/dd[1]'
    links_xpath = '//*/tr[2]/td[2]/ul/li/a'

    cover = UTA_NET + album_el.xpath(cover_xpath)[0].get('src')
    title = album_el.xpath(title_xpath)[0].text
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
        print album


if __name__ == '__main__':
    main()
