# Prompts for a search term then displays the top results from YouTube
# Work in progress, I'd like to have this be ncurses-like, and tie in with linkhandler:
# https://github.com/LukeSmithxyz/voidrice/blob/master/.local/bin/linkhandler
# TODO: https://docs.python.org/3/howto/curses.html

import requests
import json

print("Enter search term: ")
search_term = input()

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
        'date': video_renderer['publishedTimeText']['simpleText'],
        'length': video_renderer['lengthText']['simpleText'],
        'view_count': video_renderer['viewCountText']['simpleText']
        }
    print(video['title'], '|', video['author'], '|', video['length'], '|', video['view_count'], '|', video['date'], '|', video['url'])
