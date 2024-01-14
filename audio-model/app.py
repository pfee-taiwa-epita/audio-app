import streamlit as st
import pyaudio
import wave
import os

from preprocess.preprocess import preprocess_audio
from model.use_model import load_model, predict_single_audio_from_file

st.set_page_config(
    page_title='Demo Audio Model',
    page_icon="🎄",
    layout='wide',
    initial_sidebar_state='expanded',
)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 2

labels_dict = {
    0: "Accacia",
    1: "Bouleau",
    2: "Chene",
    3: "Sapin"
}

def record_preprocess(preprocess_functions, progress_bar, model) -> None:

    file_name = "original.wav"

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

    predict_label, truc = predict_single_audio_from_file(model, processed_file_name)

    cols = st.columns([3, 8])
    with cols[1]:
        st.markdown(f"# Predicted label: {labels_dict[predict_label]}")
    

    labels = ['Accacia', 'Bouleau', 'Chene', 'Sapin']
    labels_value = {
        'Accacia': truc[0][0],
        'Bouleau': truc[0][1],
        'Chene': truc[0][2],
        'Sapin': truc[0][3]
    }

    for labels, values in labels_value.items():
        if values < 0:
            labels_value[labels] = 0

    sum = 0
    for values in labels_value.values():
        sum += values

    for labels, values in labels_value.items():
        labels_value[labels] = str((values  / sum) * 100) + "%"
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Predicted logits: {truc[0]}")
        st.write(f"Predicted label index: {predict_label}")
    with col2:
        st.write(labels_value)

    os.remove("original.wav")
    os.remove("original_preprocess_audio.wav")

def main() -> None:
    st.title("Demo Audio Model 🎄")

    preprocess_functions = [preprocess_audio]
    model = load_model()

    cols = st.columns([1.5, 2, 8])
    with cols[0]:
        button = st.button("Start Recording")
    with cols[1]:
        progress_bar = st.progress(0)

    if button:
        record_preprocess(preprocess_functions, progress_bar, model)



if __name__ == "__main__":
    main()