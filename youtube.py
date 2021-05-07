# Prompts for a search term then displays the top results from YouTube with followable links
# Keybindings:
#   - INSERT mode:
#     - ESC: enter NORMAL mode
#     - ENTER: search for search term
#   - NORMAL mode:
#     - i: enter INSERT mode
#     - q: quit program
#     - j: move cursor down
#     - k: move cursor up
#     - y: open link in youtube-dl
#     - m: open link in mpv
#     - o: open link in default web browser
#     - l: open link in linkhandler
#     - c: add channel to newsboat subscriptions

import requests
import json
import curses
import os
import subprocess

os.environ['ESCDELAY'] = '25'

def searchVideos(search_term):
    r = requests.get('https://www.youtube.com/results?search_query=' + search_term.replace(' ', '+'))
    page_text = r.text
    # Probably too much text for regex to handle efficiently
    results_json_str = page_text.split('var ytInitialData = ')[1].split('</script>')[0]
    results_json_dict = json.loads(results_json_str[:-1])
    video_renderers = []
    videos = []
    section_list_renderer_contents = results_json_dict['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
    for section_list_renderer in section_list_renderer_contents:
        if 'itemSectionRenderer' in section_list_renderer:
            item_section_renderer_contents = section_list_renderer['itemSectionRenderer']['contents']
            for renderers in item_section_renderer_contents:
                # shelfRenderers contain a list of videoRenderers that can be appended to results_list
                if 'shelfRenderer' in renderers and 'verticalListRenderer' in renderers['shelfRenderer']['content']:
                    for item in renderers['shelfRenderer']['content']['verticalListRenderer']['items']:
                        video_renderers.append(item['videoRenderer'])
                # videoRenderers also exist at this level, so they too can be appended
                elif 'videoRenderer' in renderers:
                    video_renderers.append(renderers['videoRenderer'])

            for video_renderer in video_renderers:
                try:
                    video = {
                        'title': video_renderer['title']['runs'][0]['text'],
                        'url': 'https://www.youtube.com/watch?v=' + video_renderer['videoId'],
                        'channel': video_renderer['ownerText']['runs'][0]['text'],
                        'date': video_renderer['publishedTimeText']['simpleText'] if 'publishedTimeText' in video_renderer else '',
                        'length': video_renderer['lengthText']['simpleText'] if 'lengthText' in video_renderer else '',
                        'view_count': video_renderer['viewCountText']['simpleText'] if 'simpleText' in video_renderer['viewCountText'] else '',
                        'channel_url': video_renderer['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
                    }
                    if video['url'] not in [v['url'] for v in videos]:
                        videos.append(video)
                except:
                    pass
    return videos

def main(stdscr):
    k = 0
    cursor_y = 0
    cursor_x = 0
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(False)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # search bar
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW) # selected result
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # results
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # insert mode
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN) # normal mode

    insert_mode = True
    search_term = ''
    search_term_length = 0
    videos = []

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k in (curses.KEY_ENTER, 10, 13):
            if cursor_y == 0:
                videos = searchVideos(search_term)
                insert_mode = False
                cursor_y = 1
        if insert_mode:
            if k == 27: # switch to normal mode if esc is pressed
                insert_mode = False
                cursor_y = 1
            elif k == curses.KEY_BACKSPACE and len(search_term) > 0: # delete the last character
                search_term = search_term[:-1]
                cursor_x -= 1
            elif k >= 32 and k <= 126: # accept any typeable character
                search_term += chr(k)
                cursor_x += 1
        else: # normal mode
            if cursor_y > 0 and len(videos) > 0:
                url = videos[cursor_y-1]['url']
                channel_url = videos[cursor_y-1]['channel_url']
                if channel_url.startswith('/user/'):
                    rss_url = 'https://www.youtube.com/feeds/videos.xml?user=' + channel_url.replace('/user/', '')
                else:
                    rss_url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_url.replace('/channel/', '') + '\n'
                FNULL = open(os.devnull, 'w')
                if k == ord('y'): # open with youtube-dl
                    subprocess.call(['youtube-dl', url], stdout=FNULL, stderr=subprocess.STDOUT)
                elif k == ord('m'): # open with mpv
                    subprocess.call(['mpv', url], stdout=FNULL, stderr=subprocess.STDOUT)
                elif k == ord('o'): # open with $BROWSER
                    browser = os.getenv('BROWSER')
                    subprocess.call([browser, url], stdout=FNULL, stderr=subprocess.STDOUT)
                elif k == ord('l'): # open with linkhandler
                    subprocess.call(['linkhandler', url], stdout=FNULL, stderr=subprocess.STDOUT)
                elif k == ord('c'): # add channel to newsboat subscriptions
                    urls_filename = os.getenv('HOME') + '/.config/newsboat/urls'
                    urls_file_contents = ''
                    with open(urls_filename, 'r') as urls_file:
                        urls_file_contents = urls_file.read()
                    if rss_url not in urls_file_contents:
                        with open(urls_filename, 'a') as urls_file:
                            urls_file.write(rss_url + '\n')

            if k == ord('i'): # switch to insert mode
                cursor_y = 0
                insert_mode = True
            elif k == ord('j'): # cursor down
                cursor_y += 1
                cursor_y = min(min(len(videos), height - 2), cursor_y)
            elif k == ord('k'): # cursor up
                cursor_y -= 1
                cursor_y = max(0, cursor_y)
                if cursor_y == 0:
                    insert_mode = True
            elif k == ord('q'): # quit
                break

        for i, video in enumerate(videos):
            if i < height - 2:
                video_str = video['title'] + ' | ' + video['channel'] + ' | ' + video['length'] + ' | ' + video['view_count'] + ' | ' + video['date']
                video_str = video_str[:width-2]
                if cursor_y - 1 == i:
                    stdscr.attron(curses.color_pair(2))
                else:
                    stdscr.attron(curses.color_pair(3))
                stdscr.addstr(i+1, 0, video_str)
                stdscr.addstr(i+1, len(video_str), " " * (width - len(video_str) - 1))
                if cursor_y - 1 == i:
                    stdscr.attroff(curses.color_pair(2))
                else:
                    stdscr.attroff(curses.color_pair(3))

        status_text = 'INSERT' if insert_mode else 'NORMAL'

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, 0, search_term)
        stdscr.attroff(curses.color_pair(1))

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, len(search_term), " ")
        stdscr.attroff(curses.color_pair(3))

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, len(search_term) + 1, " " * (width - len(search_term) - 2))
        stdscr.attroff(curses.color_pair(1))

        if insert_mode:
            stdscr.attron(curses.color_pair(4))
        else:
            stdscr.attron(curses.color_pair(5))
        stdscr.addstr(height-1, 0, status_text)
        stdscr.addstr(height-1, len(status_text), " " * (width - len(status_text) - 1))
        if insert_mode:
            stdscr.attroff(curses.color_pair(4))
        else:
            stdscr.attroff(curses.color_pair(5))

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()

curses.wrapper(main)
