# Given the link to an album page on Bandcamp, make a local album directory, fetch the mp3 files, and download the files to the directory

import requests
import json
import sys
import os

for url in sys.argv[1:]:
    r = requests.get(url)
    pageText = r.text
    trackInfo = pageText.split('trackinfo: ')[1].split(',\n')[0]
    tracks = json.loads(trackInfo)
    album = url.split('/')[-1]
    os.mkdir(album)
    for track in tracks:
        filename = album + '/' + str(track['track_num']) + ' - ' + track['title'].replace('/', '-') + '.mp3'
        print('Downloading', filename, '...')
        mp3file = requests.get(track['file']['mp3-128'])
        with open(filename, 'wb') as fd:
            for chunk in mp3file.iter_content(chunk_size=128):
                fd.write(chunk)
