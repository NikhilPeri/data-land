from pydub import AudioSegment
from pydub.playback import play


def split_vocals(mp3_file):
    sound_stereo = AudioSegment.from_file(mp3_file, format="mp3")
    sound_monoL = sound_stereo.split_to_mono()[0]
    sound_monoR = sound_stereo.split_to_mono()[1]

    sound_monoR_inv = sound_monoR.invert_phase()

    vocals = 
    beat = sound_monoL.overlay(sound_monoR_inv)
