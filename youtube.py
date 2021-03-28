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
results_list = []
item_section_renderer_contents = results_json_dict['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

for isr_content in item_section_renderer_contents:
    # shelfRenderers contain a list of videos that can be concatenated to results_list
    if 'shelfRenderer' in isr_content:
        results_list += isr_content['shelfRenderer']['content']['verticalListRenderer']['items']
    # videoRenderers are what we're looking for, so those can be appended individually
    elif 'videoRenderer' in isr_content:
        results_list.append(isr_content)

for result in results_list:
    video = {
        'video_title': result['videoRenderer']['title']['runs'][0]['text'],
        'video_url': 'https://www.youtube.com/watch?v=' + result['videoRenderer']['videoId'],
        'video_author': result['videoRenderer']['ownerText']['runs'][0]['text'],
        'video_date': result['videoRenderer']['publishedTimeText']['simpleText'],
        'video_length': result['videoRenderer']['lengthText']['simpleText'],
        'video_view_count': result['videoRenderer']['viewCountText']['simpleText']
        }
    print(video)
