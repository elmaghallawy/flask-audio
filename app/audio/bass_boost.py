from pydub import AudioSegment
from os import listdir
import numpy as np
import math
from pathlib import Path


# Path(__file__).parent.parent.parent.absolute().joinpath(
#     'media/audio/uploads')  # "songs"
# print(song_dir)
attenuate_db = 0
accentuate_db = 2

def bass_line_freq(track):
    sample_track = list(track)

    # c-value
    est_mean = np.mean(sample_track)

    # a-value
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor


# for filename in listdir(song_dir):
def export_bass_boosted(song_dir, filename):
    """functio the returns a bass boosted track 

    Args:
        song_dir (path): a path for the directory containing the audio file
        filename (string): the name of the audio file
    """
    sample = AudioSegment.from_mp3(str(song_dir) + "/" + filename)
    filtered = sample.low_pass_filter(
        bass_line_freq(sample.get_array_of_samples()))

    combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
    combined.export(Path(__file__).parent.parent.parent.absolute().joinpath(
        'media/audio/exports/' + (filename.replace(".mp3",
                                                    "") + "-export.mp3")), format="mp3")
