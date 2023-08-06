import os
import subprocess

import soundfile as sf
from gtts import gTTS
from pydub import AudioSegment


def export_audio_files(output_audio_file, merge_sounds):
    merge_sounds.export(output_audio_file, format="wav")


def merge_audio_files(audio_files):
    merge_sounds = AudioSegment.from_wav(audio_files[0])
    for audio_file in audio_files[1:]:
        merge_sounds += AudioSegment.from_wav(audio_file)
    return merge_sounds


def get_duration(audio_file):
    sound_file = sf.SoundFile(audio_file)
    duration = len(sound_file) / sound_file.samplerate
    return duration


def format_duration(duration):
    return '{:.2f}s'.format(duration)


def convert_string_to_wav(text, outfile_path, lang='en', delay=0, tempo=1.2):
    gTTS(text=text, lang=lang, slow=False).save(outfile_path + '.tmp.mp3')
    subprocess.call(
        ["mpg123", "-w", outfile_path + '.tmp.wav', outfile_path + '.tmp.mp3'],
        stdout=open(os.devnull, "w"),
        stderr=subprocess.STDOUT)
    subprocess.call([
        "sox", outfile_path + '.tmp.wav', outfile_path, "tempo",
        str(tempo), "delay",
        str(delay)
    ],
                    stdout=open(os.devnull, "w"),
                    stderr=subprocess.STDOUT)
    os.remove(outfile_path + '.tmp.wav')
    os.remove(outfile_path + '.tmp.mp3')
