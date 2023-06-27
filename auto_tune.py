from pathlib import Path
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import psola



def closest_pitch(pitch):
    sounds = np.around(librosa.hz_to_midi(pitch))
    inne = np.isnan(pitch)
    sounds[inne] = np.nan
    return librosa.midi_to_hz(sounds)



def autotune(audio, sr):
    frame_length = 2048
    hop_length = frame_length // 4
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')

    pitch, _, _ = librosa.pyin(audio, frame_length=frame_length, hop_length=hop_length, sr=sr, fmin=fmin, fmax=fmax)

    corrected_pitch = closest_pitch(pitch)

    return psola.vocode(audio, sample_rate=int(sr), target_pitch=corrected_pitch, fmin=fmin, fmax=fmax)


def main():

    path_to_file = Path("plik.wav")
    y, sr = librosa.load(str(path_to_file), sr=None, mono=False)
    if y.ndim > 1:
        y = y[0, :]


    betterpitch = autotune(y, sr)

    sf.write("new_test.wav", betterpitch, sr)
    




