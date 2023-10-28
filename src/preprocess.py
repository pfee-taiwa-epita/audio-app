import numpy as np
from scipy.interpolate import interp1d
from scipy.io import wavfile
import librosa
import soundfile as sf

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

def preprocess_audio_2(file_path):
    function_name = "preprocess_audio_2"
    # Load audio file
    y, sr = librosa.load(file_path, sr=None, mono=False)
    # Convert to mono
    y_mono = librosa.to_mono(y)
    # Resample to 16 kHz
    y_resampled = librosa.resample(y_mono, orig_sr=sr, target_sr=16000)
    #y_resampled = librosa.resample(y_mono, sr, 16000)
    # Pad/trim to 3 seconds (3 * 16 kHz = 48000 samples)
    if len(y_resampled) < 48000:
        y_padded = librosa.util.pad_center(y_resampled, 48000)
    else:
        y_padded = y_resampled[:48000]
    # Save the preprocessed audio to 16-bit PCM WAV format
    sf.write(file_path + "_" + function_name + ".wav", y_padded, 16000, subtype='PCM_16')

