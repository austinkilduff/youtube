# Prompts for a search term then displays the top results from YouTube
# Work in progress, I'd like to have this be ncurses-like, and tie in with linkhandler:
# https://github.com/LukeSmithxyz/voidrice/blob/master/.local/bin/linkhandler
# TODO: https://docs.python.org/3/howto/curses.html

import requests
import json
import curses
import os

# TODO: these aren't helping ESCAPE delay
os.environ['ESCDELAY'] = '25'
os.environ.setdefault('ESCDELAY', '25')

def searchVideos(search_term):
    r = requests.get('https://www.youtube.com/results?search_query=' + search_term.replace(' ', '+'))
    page_text = r.text
    # Probably too much text for regex to handle efficiently
    results_json_str = page_text.split('var ytInitialData = ')[1].split('</script>')[0]
    results_json_dict = json.loads(results_json_str[:-1])
    video_renderers = []
    item_section_renderer_contents = results_json_dict['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

    for renderers in item_section_renderer_contents:
        # shelfRenderers contain a list of videoRenderers that can be appended to results_list
        if 'shelfRenderer' in renderers:
            for item in renderers['shelfRenderer']['content']['verticalListRenderer']['items']:
                video_renderers.append(item['videoRenderer'])
        # videoRenderers also exist at this level, so they too can be appended
        elif 'videoRenderer' in renderers:
            video_renderers.append(renderers['videoRenderer'])

    for video_renderer in video_renderers:
        video = {
            'title': video_renderer['title']['runs'][0]['text'],
            'url': 'https://www.youtube.com/watch?v=' + video_renderer['videoId'],
            'author': video_renderer['ownerText']['runs'][0]['text'],
            'date': video_renderer['publishedTimeText']['simpleText'] if 'publishedTimeText' in video_renderer else '',
            'length': video_renderer['lengthText']['simpleText'],
            'view_count': video_renderer['viewCountText']['simpleText']
        }
        return video

def main(stdscr):
    k = 0
    cursor_y = 0
    cursor_x = 0
    curses.cbreak()
    stdscr.keypad(True)

    insert_mode = True
    search_term = ''
    search_term_length = 0
    running = True
    videos = []

    while running:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_ENTER and cursor_y == 0:
            search_term = stdscr.getstr(0, 0, len(search_term)-1)
            videos = searchVideos(search_term)
        if insert_mode:
            if k == 27: # switch to normal mode if esc is pressed
                insert_mode = False
            elif k == curses.KEY_BACKSPACE and len(search_term) > 0: # delete the last character
                search_term = search_term[:-1]
                cursor_x -= 1
            elif k >= 32 and k <= 126: # accept any typeable character
                search_term += chr(k)
                cursor_x += 1
        else: # normal mode
            if k == ord('i'): # switch to insert mode
                insert_mode = True
            elif k == ord('j'): # cursor down
                cursor_y += 1
                cursor_y = min(height-1, cursor_y)
            elif k == ord('k'): # cursor up
                cursor_y -= 1
                cursor_y = max(0, cursor_y)
            elif k == ord('q'): # quit
                running = False

        # TODO: if videos is not empty, print contents
        for video in videos:
            video_str = video['title'] + '|' + video['author'] + '|' + video['length'] + '|' + video['view_count'] + '|' + video['date'] + '|' + video['url']

        status_text = 'INSERT' if insert_mode else 'NORMAL'

        stdscr.addstr(0, 0, search_term)
        stdscr.addstr(height-1, 0, status_text)
        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()

curses.wrapper(main)
