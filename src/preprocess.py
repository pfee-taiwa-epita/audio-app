import numpy as np
from scipy.interpolate import interp1d
from scipy.io import wavfile
import librosa
import soundfile as sf

from src.audioprocessor import AudioPreprocessor

def apply_transfer(signal, transfer, interpolation='linear'):
    constant = np.linspace(-1, 1, len(transfer))
    interpolator = interp1d(constant, transfer, interpolation)
    return interpolator(signal)

def limiter(x, threshold=0.8):
    transfer_len = 1000
    transfer = np.concatenate([ np.repeat(-1, int(((1-threshold)/2)*transfer_len)),
                                np.linspace(-1, 1, int(threshold*transfer_len)),
                                np.repeat(1, int(((1-threshold)/2)*transfer_len)) ])
    return apply_transfer(x, transfer)

def arctan_compressor(x, factor=2):
    constant = np.linspace(-1, 1, 1000)
    transfer = np.arctan(factor * constant)
    transfer /= np.abs(transfer).max()
    return apply_transfer(x, transfer)

def preprocess_audio(file_path):
    function_name = "preprocess_audio"
    sr, x = wavfile.read(file_path)
    x = x / np.abs(x).max()
    x3 = arctan_compressor(x)
    x3 = np.int16(x3 * 32767)

    file_path = file_path.split(".wav")[0]

    wavfile.write(file_path + "_" + function_name + ".wav", sr, x3)


'''
TypeError: pad_center() takes 1 positional argument but 2 were given
Traceback:
File "/Users/stanley.schillaci/.pyenv/versions/3.10.13/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 541, in _run_script
    exec(code, module.__dict__)
File "/Users/stanley.schillaci/Document/epita/PFEE/audio-sampler-v2/pages/preprocess_📈.py", line 92, in <module>
    main()
File "/Users/stanley.schillaci/Document/epita/PFEE/audio-sampler-v2/pages/preprocess_📈.py", line 87, in main
    record_preprocess(preprocess_functions, progress_bar)
File "/Users/stanley.schillaci/Document/epita/PFEE/audio-sampler-v2/pages/preprocess_📈.py", line 60, in record_preprocess
    preprocess_function(file_name)
File "/Users/stanley.schillaci/Document/epita/PFEE/audio-sampler-v2/src/preprocess.py", line 44, in preprocess_audio_2
    y_padded = librosa.util.pad_center(y_resampled, 48000)
'''

# def preprocess_audio_2(file_path):
#     function_name = "preprocess_audio_2"
#     y, sr = librosa.load(file_path, sr=None, mono=False)
#     y_mono = librosa.to_mono(y)
#     y_resampled = librosa.resample(y_mono, orig_sr=sr, target_sr=16000)
#     if len(y_resampled) < 48000:
#         y_padded = librosa.util.pad_center(y_resampled, 48000)
#     else:
#         y_padded = y_resampled[:48000]
#     sf.write(file_path + "_" + function_name + ".wav", y_padded, 16000, subtype='PCM_16')


'''
Ton fichier se nomme "original.wav_preprocess_audio_3.wav"
Renome le en "original_preprocess_audio_3.wav"

De plus il a une duree de 10 secondes au lieu de 2 secondes...
'''

def preprocess_audio_3(file_path):
    function_name = "preprocess_audio_3"
    y, sr = librosa.load(file_path, sr=None, mono=False)
    y_mono = librosa.to_mono(y)
    p = AudioPreprocessor()
    audio = p.preprocess(y_mono, sr)
    sf.write(file_path + "_" + function_name + ".wav", audio, 16000, subtype='PCM_16')