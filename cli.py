from difflevel import DiffLevel
    
def get_diff(expected_diff: DiffLevel | None) -> DiffLevel:
    '''Ask the user which difficulty level the diff is at.
    
    `expected_diff`: The default option, selected with an empty input.
    '''
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

def yesno(prompt: str, default: bool) -> bool:
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
    
def select_option(prompt: str, *options, default: int = None):
    '''Ask the user to select an option from a list.

    The options are presented in a numbered list starting at 0 and the user is
    asked to enter one of the numbers.
    Any other input selects the default option.
    
    `prompt`: A message shown to the user alongside the options.
    `default`: The index of the default option.
    `options`: Any number of options to choose from. Any types will work, but
    their string representations should be sensible and concise.
    '''
    num_options = len(options)
    option_list = {str(i): options[i] for i in range(num_options)}
    
    print(prompt + '\n')
    for (number, option) in option_list.items():
        print(f'{number}: {option}')

    answer = input(f'\nEnter a number (0-{num_options-1}): ')
    if answer in option_list.keys():
        return option_list[answer]
    else:
        return option_list[str(default)]
