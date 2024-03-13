import difflevel
from difflevel import DiffLevel
import json
from ossapi import Ossapi
from ossapi.enums import RankStatus
import pyperclip as clipboard

    
def prompt_diff(expected_diff: DiffLevel | None) -> DiffLevel:
    if expected_diff is None:
        prompt = 'Diff level: '
    else:
        prompt = f'Diff level [{expected_diff.value}]: '

    while True: # prompt until valid input
        diff_str = input(prompt).lower()
        if expected_diff and not diff_str: # user accepted 'default' with enter
            return expected_diff
        else:
            diff = DiffLevel.from_str(diff_str)
            if diff:
                return diff

def prompt_yesno(prompt: str, default: bool) -> bool:
    '''Ask the user a yes/no question.
    
    Adds "` (Y/n) [y]: `" or "` (y/N): `" to `prompt` based on `default`.
    '''
    answer_hint = '(Y/n)' if default else '(y/N)'
    answer = input(f'{prompt} {answer_hint}')
    if answer in ['y', 'yes']:
        return True
    elif answer in ['n', 'no']:
        return False
    else:
        return default

def main():
    with open('credentials.json') as client_file:
        client = json.load(client_file)
    api = Ossapi(client['id'], client['secret'])
    
    map_link = input('Map link: ')
    map_id = int(map_link.split('/')[-1])
    map = api.beatmap(map_id)
    mapset = map.beatmapset()

    expected_diff = difflevel.expected_diff(map)
    diff = prompt_diff(expected_diff)
    
    use_unicode_artist = prompt_yesno('Unicode artist?', False)
    use_unicode_title = prompt_yesno('Unicode title?', False)
    
    artist = mapset.artist if not use_unicode_artist else mapset.artist_unicode
    title = mapset.title if not use_unicode_title else mapset.title_unicode

    bb_img = f'[img]{diff.image_url()}[/img]'
    bb_title = f'{artist} - [b]{title}[/b] [{map.version}]'
    bb_url = f'[url={map_link}]{bb_img} {bb_title}[/url]'
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
