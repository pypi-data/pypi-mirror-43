import mistune


def extract_script(text):
    renderer = Renderer()
    markdown = mistune.Markdown(renderer=renderer)
    markdown(text)

    return renderer.script_parts


class Renderer(mistune.Renderer):
    def __init__(self, **kwargs):
        self.script_parts = []
        super(Renderer, self).__init__(**kwargs)

    def paragraph(self, text):
        self.script_parts.append(text)
        return ''
