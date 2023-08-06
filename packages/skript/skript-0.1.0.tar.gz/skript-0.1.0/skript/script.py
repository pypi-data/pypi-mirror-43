import textwrap


def export_script(script_output, text):
    text_cutted = '\n'.join(textwrap.wrap(text, 80, break_long_words=False))
    with open(script_output, 'w') as stream:
        stream.write(text_cutted)
