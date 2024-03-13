import cli
import difflevel
import json
from ossapi import Ossapi
from ossapi.enums import RankStatus
import pyperclip as clipboard


def main():
    with open('credentials.json') as client_file:
        client = json.load(client_file)
    api = Ossapi(client['id'], client['secret'])
    
    map_link = input('Map link: ')
    map_id = int(map_link.split('/')[-1])
    map = api.beatmap(map_id)

    # intuit and confirm the level of the diff
    expected_diff = difflevel.expected_diff(map)
    diff = cli.get_diff(expected_diff)
    
    # decide whether to use unicode or romanised artist and title fields
    mapset = map.beatmapset()

    if mapset.artist != mapset.artist_unicode:
        artist = cli.select_option(
            "Unicode or romanised artist?",
            mapset.artist_unicode,
            mapset.artist,
            default=0
        )
    else:
        artist = mapset.artist

    if mapset.title != mapset.title_unicode:
        title = cli.select_option(
            "Unicode or romanised title?",
            mapset.title_unicode,
            mapset.title,
            default=0
        )
    else:
        title = mapset.title

    # build the bbcode of the entry
    bb_img = f'[img]{diff.image_url()}[/img]'
    bb_title_row = f'{artist} - [b]{title}[/b] [{map.version}]'
    bb_url = f'[url={map_link}]{bb_img} {bb_title_row}[/url]'
    bb_ranked_tag = ' [b]Ranked[/b]' if map.ranked == RankStatus.RANKED else ''
    final_bbcode = '\n\n' + bb_url + bb_ranked_tag

    print(final_bbcode + '\n')
    try:
        clipboard.copy(final_bbcode)
        print('(copied to clipboard)')
    except:
        print('(failed to copy to clipboard)')


if __name__ == '__main__':
    main()
