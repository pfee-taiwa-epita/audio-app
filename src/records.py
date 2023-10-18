import pyaudio
import wave
import streamlit as st
import uuid
import datetime
import socket

from io import BytesIO

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 3


def record(label_name, nb_sample):

    for i in range(nb_sample):
        unique_id = str(uuid.uuid4())

        current_datetime = datetime.datetime.now()
        date_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            my_bar = st.progress(0)
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                my_bar.progress(i * 2.16 / 100)
                data = stream.read(CHUNK)
                frames.append(data)
            my_bar.progress(100)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        audio_data = BytesIO()
        with wave.open(audio_data, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        file_name = f"{label_name}-{unique_id}.wav"

        ip_address = socket.gethostbyname(socket.gethostname())

        if label_name not in st.session_state['audio_files']:
            st.session_state['audio_files'][label_name] = []
        st.session_state['audio_files'][label_name].append((file_name, audio_data, current_datetime.timestamp(), date_str, unique_id, ip_address))

        with col2:
            st.audio(audio_data, format='audio/wav', start_time=0)
        with col3:     
            st.success('Record Success !', icon="✅")

    st.session_state['is_recording'] = False
    st.session_state['progression'] = 0