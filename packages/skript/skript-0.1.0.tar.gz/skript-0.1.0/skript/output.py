import textwrap

import termcolor


def print_title(text, character='-', before='', after=''):
    print(
        termcolor.colored(
            '{} {} {}'.format(before, text, after).center(80, character),
            'green'))


def print_text(text):
    text_cutted = '\n'.join(textwrap.wrap(text, 80, break_long_words=False))
    print(termcolor.colored(text_cutted, 'cyan'))
