import pyaudio
import wave
import streamlit as st
import uuid
import datetime
import socket

from io import BytesIO

from src.gdrive import write_file_to_gdrive

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 3


def record(label_name, nb_sample) -> None:

    for i in range(nb_sample):
        metadata = {}
        metadata['id'] = str(uuid.uuid4())

        current_datetime = datetime.datetime.now()
        metadata['date'] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        metadata['timestamp'] = current_datetime.timestamp()

        metadata['user'] = socket.gethostbyname(socket.gethostname())
        metadata['label'] = label_name

        file_name = f"{label_name}/{label_name}-{metadata['id']}.wav"
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
        
        with col2:
            st.audio(audio_data, format='audio/wav', start_time=0)
        with col3:     
            st.success('Record Success !', icon="✅")

        write_file_to_gdrive(file_name, audio_data, metadata)
        
    st.session_state['is_recording'] = False
    st.session_state['progression'] = 0