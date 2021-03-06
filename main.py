import requests
from bs4 import BeautifulSoup
from urllib import request
import re
import os
import sys


def scrape_xkcd(download_number=0):
    if len(sys.argv) >= 2:
        download_number = int(sys.argv[1])
    comic_tracker = download_number
    try:
        os.mkdir("XKCD")
    except FileExistsError:
        pass
    if download_number != 0:
        end_early = True
    else:
        end_early = False
        comic_tracker += 1
    next_accesskey = 'first'
    while True:
        if comic_tracker != 1525:
            url = 'http://www.xkcd.com/' + str(comic_tracker)
            response = requests.get(url)
            html = response.content

            soup = BeautifulSoup(html, "html.parser")
            next_find = soup.find('a', href='#')
            if next_find is not None:
                next_accesskey = next_find['accesskey']
            table = soup.find(id="comic")
            if table is None or table.img is None or table.img.findChildren('alt'):
                comic_tracker += 1
                continue
            img_name = table.img['alt']
            img_name = re.sub("[^0-9a-zA-Z\s]+", "", img_name)
            img = table.img['src']
            xkcd_alt = table.img['title']
            xkcd_alt = ''.join([i if ord(i) < 128 else '*' for i in xkcd_alt])
            xkcd_alt_file_name = re.sub("[^0-9a-zA-Z\s]+", "*", xkcd_alt)
            img_url = img[2:]
            img_url = "http://www." + img_url
            img_ext = img[len(img)-4:]
            print(img_url)
            g = request.urlopen(img_url)
            with open(os.path.join("XKCD", img_name + img_ext), 'b+w') as f:
                f.write(g.read())
                print("Successfully downloaded " + img_name + " - #" + str(comic_tracker))
            with open(os.path.join("XKCD", img_name + ".txt"), 'w') as f:
                f.write(xkcd_alt_file_name)
                print("Saved alt-text")
            if next_accesskey == ['n']:
                return 0
        comic_tracker += 1
        if end_early:
            break

if __name__ == '__main__':
    scrape_xkcd()
