import pyaudio
import wave
import streamlit as st
import uuid
import datetime
import socket
import uuid
import hashlib

from src.dataset import push_files_to_hub, add_data_info
from src.preprocess import preprocess_audio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 2

def record(label_name, nb_sample) -> None:
    WAVE_OUTPUT_FOLDER = st.session_state['wave_output_folder']
    all_metadata = []

    for i in range(nb_sample):
        current_datetime = datetime.datetime.now()

        metadata = {}

        metadata['file_id'] = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:8]
        metadata['label'] = label_name
        metadata['user_name'] = st.session_state['user_name']
        metadata['user_ip'] = socket.gethostbyname(socket.gethostname())
        metadata['date'] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        metadata['timestamp'] = current_datetime.timestamp()
        metadata['filename'] = f"{label_name}-{metadata['file_id']}.wav"
        metadata['hugging_face_link'] = "https://huggingface.co/datasets/" + st.session_state['hugging_face_repo'] +"/blob/main/data/" + label_name.lower() + "/" + metadata['filename']

        file_name = WAVE_OUTPUT_FOLDER + f"{label_name}-{metadata['file_id']}.wav"


        all_metadata.append(metadata)

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        cols = st.columns([2, 8, 2])
        with cols[0]:
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
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        audio_file = open(file_name, 'rb')
        audio_bytes = audio_file.read()
        audio_file.close()
        
        with cols[1]:
            st.audio(audio_bytes, format='audio/wav', start_time=0)
        with cols[2]:     
            st.success('Record Success !', icon="✅")

    with st.status("Uploading data...", expanded=True) as status:
        st.write("Uploading metadata")
        add_data_info(all_metadata)
        st.write("Uploading audio files")
        push_files_to_hub(label_name)

    status.update(label="Download complete!", state="complete", expanded=False)

    st.session_state['is_recording'] = False