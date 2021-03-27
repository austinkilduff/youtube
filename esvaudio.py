# Download all Bible chapters as mp3 from the English Standard Version website

import requests

# Use this as a reference for all books and chapter numbers
kjv_url = 'https://raw.githubusercontent.com/honza/bibles/master/KJV/KJV.json'
r = requests.get(kjv_url)
bible = r.json()
for book in bible.keys():
    for chapter in bible[book].keys():
        filename = book + ' ' + chapter + '.mp3'
        audio_url = 'https://audio.esv.org/hw/mq/' + filename
        mp3file = requests.get(audio_url)
        with open(filename, 'wb') as fd:
            for chunk in mp3file.iter_content(chunk_size=128):
                fd.write(chunk)
