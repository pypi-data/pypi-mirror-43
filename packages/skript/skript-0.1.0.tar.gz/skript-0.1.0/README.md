# Skript

**Skript** is a python tool that will help your work process whan you made video.

**Skript** convert markdown into a raw text file (`.txt`) that you can use for a teleprompter
and also an audio file (`.wav`) with the script pronounced by the google synthetic voice.
You can use **Skript** to time your speeches.

## Quickstart

**Skript** can be installed with `pip3`.

    pip3 install skript

Write a markdown file and run **Skript** on it.

    skript script.md

## Options

### Output

By default the files will created with the name `output`.
You can change this the option `-o` or `--output`.

    skript sckript -o <custom name>

### Tempo

You can choose the tempo (default: 1.35)

    skript sckript -t <tempo>

### Language

You can choose the language used for speech generation.

    skript script.md -l <language key>

[language key] can be fr (french), en, es (spanish), zh-CN (chinese), ... Complete list can be found [here](https://pypi.python.org/pypi/gTTS)

### Cache

**Skript** use a cache to generate temporary audio files and do not regenerate two times the same file.
You can clean the cache with.

    skript script.md --clean-cache
