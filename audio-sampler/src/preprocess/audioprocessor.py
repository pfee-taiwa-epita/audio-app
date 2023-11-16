import numpy as np
import librosa
import scipy.signal

class AudioPreprocessor:
    def __init__(self, target_sample_rate=16000, filter_type='lowpass', cutoff_freq=4000, max_audio_length=160000):
        self.target_sample_rate = target_sample_rate
        self.filter_type = filter_type
        self.cutoff_freq = cutoff_freq
        self.max_audio_length = max_audio_length

    def _apply_filter(self, audio_data):
        if self.filter_type == 'lowpass':
            b, a = scipy.signal.butter(
                4, self.cutoff_freq, fs=self.target_sample_rate, btype='low')
            filtered_audio = scipy.signal.lfilter(b, a, audio_data)
            return filtered_audio
        else:
            return audio_data
        
    def _resample(self, audio_data, sample_rate):
        if sample_rate != self.target_sample_rate:
            resampled_audio = librosa.resample(
                audio_data, orig_sr=sample_rate, target_sr=self.target_sample_rate)
            return resampled_audio
        else:
            return audio_data
        
    def preprocess(self, audio_data, sample_rate):
        filtered_audio = self._apply_filter(audio_data)
        if sample_rate != self.target_sample_rate:
            audio_data = self._resample(audio_data, sample_rate)
        silence_duration = int(0.5 * self.target_sample_rate)
        resampled_audio = np.pad(
            filtered_audio, (silence_duration, silence_duration), mode='constant')
        if len(resampled_audio) < self.max_audio_length:
            padding_needed = self.max_audio_length - len(resampled_audio)
            resampled_audio = np.pad(
                resampled_audio, (0, padding_needed), mode='constant')
        elif len(resampled_audio) > self.max_audio_length:
            resampled_audio = resampled_audio[:self.max_audio_length]
        if resampled_audio.dtype != np.int16:
            resampled_audio = (resampled_audio * 32767).astype(np.int16)
        else:
            resampled_audio = resampled_audio
        return resampled_audio
    
    def convert_to_model_input(self, audio_data):
        mel_spec = librosa.feature.melspectrogram(
            y=audio_data, sr=self.target_sample_rate)
        log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
        return log_mel_spec