import streamlit as st
import pyaudio
import wave
import os

from src.utils import keep_session_state_between_pages
from src.preprocess import preprocess_audio #, preprocess_audio_2, preprocess_audio_3

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 2

def record_preprocess(preprocess_functions, progress_bar) -> None:
    WAVE_OUTPUT_FOLDER = "./preprocess/"

    file_name = WAVE_OUTPUT_FOLDER + "original.wav"

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    progress_bar.progress(0)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        progress_bar.progress(i * 2.16 / 100)
        data = stream.read(CHUNK)
        frames.append(data)
    progress_bar.progress(100)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


    audio_file = open(file_name, 'rb')
    audio_bytes = audio_file.read()
    audio_file.close()
    cols = st.columns([3, 8])
    with cols[0]:
        st.write("Original")
    with cols[1]:
        st.audio(audio_bytes, format='audio/wav', start_time=0)

    for preprocess_function in preprocess_functions:
        file_without_extension = file_name.split(".wav")[0]
        processed_file_name = file_without_extension + f"_{preprocess_function.__name__}.wav"
        preprocess_function(file_name)
        audio_file = open(processed_file_name, 'rb')
        audio_bytes = audio_file.read()
        audio_file.close()
        cols = st.columns([3, 8])
        with cols[0]:
            st.write(preprocess_function.__name__)
        with cols[1]:
            st.audio(audio_bytes, format='audio/wav', start_time=0)

    files = [WAVE_OUTPUT_FOLDER + f for f in os.listdir(WAVE_OUTPUT_FOLDER) if os.path.isfile(os.path.join(WAVE_OUTPUT_FOLDER, f))]
    for f in files:
        os.remove(f)

def main() -> None:
    keep_session_state_between_pages(key_suffix='')
    st.title("Listen to preprocessed audio files 📈")

    preprocess_functions = [preprocess_audio] #, preprocess_audio_2, preprocess_audio_3]

    cols = st.columns([1.5, 2, 8])
    with cols[0]:
        button = st.button("Start Recording")
    with cols[1]:
        progress_bar = st.progress(0)

    if button:
        record_preprocess(preprocess_functions, progress_bar)



if __name__ == "__main__":
    main()