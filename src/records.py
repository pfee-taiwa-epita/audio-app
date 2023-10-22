import pyaudio
import wave
import streamlit as st
import uuid
import datetime
import socket
import uuid
import hashlib

from src.dataset import push_files_to_hub

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 3

def record(label_name, nb_sample) -> None:
    WAVE_OUTPUT_FOLDER = st.session_state['wave_output_folder']

    for i in range(nb_sample):
        metadata = {}
        metadata['id'] = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:8]

        current_datetime = datetime.datetime.now()
        metadata['date'] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        metadata['timestamp'] = current_datetime.timestamp()

        metadata['user'] = socket.gethostbyname(socket.gethostname())
        metadata['label'] = label_name

        file_name = WAVE_OUTPUT_FOLDER + f"{label_name}-{metadata['id']}.wav"
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

        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)

        for key, value in metadata.items():
            metadata_str = f"{key}: {value}\n"
            waveFile.writeframes(metadata_str.encode())


        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        audio_file = open(file_name, 'rb')
        audio_bytes = audio_file.read()
        audio_file.close()
        
        with col2:
            st.audio(audio_bytes, format='audio/wav', start_time=0)
        with col3:     
            st.success('Record Success !', icon="✅")
    
    push_files_to_hub()

    st.session_state['is_recording'] = False
    st.session_state['progression'] = 0