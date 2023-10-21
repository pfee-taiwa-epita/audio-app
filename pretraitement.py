import numpy as np
#import librosa
#%matplotlib inline
import matplotlib.pyplot as plt
#import librosa.display
from scipy.interpolate import interp1d
from scipy.io import wavfile

def apply_transfer(signal, transfer, interpolation='linear'):
    constant = np.linspace(-1, 1, len(transfer))
    interpolator = interp1d(constant, transfer, interpolation)
    return interpolator(signal)

# hard limiting
def limiter(x, treshold=0.8):
    transfer_len = 1000
    transfer = np.concatenate([ np.repeat(-1, int(((1-treshold)/2)*transfer_len)),
                                np.linspace(-1, 1, int(treshold*transfer_len)),
                                np.repeat(1, int(((1-treshold)/2)*transfer_len)) ])
    return apply_transfer(x, transfer)

# smooth compression: if factor is small, its near linear, the bigger it is the
# stronger the compression
def arctan_compressor(x, factor=2):
    constant = np.linspace(-1, 1, 1000)
    transfer = np.arctan(factor * constant)
    transfer /= np.abs(transfer).max()
    return apply_transfer(x, transfer)

def traitement(enregistrement):
    sr, x = wavfile.read(enregistrement)
    x = x / np.abs(x).max() # x scale between -1 and 1
    x2 = limiter(x)
    x2 = np.int16(x2 * 32767)
    wavfile.write("output_limit.wav", sr, x2)
    x3 = arctan_compressor(x)
    x3 = np.int16(x3 * 32767)
    wavfile.write("output_comp.wav", sr, x3)
    r = "output_comp.wav"
    return r

audio = traitement("Nouvel enregistrement.wav")