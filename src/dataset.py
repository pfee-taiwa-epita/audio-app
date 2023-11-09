import pandas as pd
import os
import streamlit as st
import soundfile as sf
import re

from huggingface_hub import HfApi, snapshot_download


def push_files_to_hub(label: str) -> None:
    api = HfApi()
    WAVE_OUTPUT_FOLDER = st.session_state['wave_output_folder']
    REPO_FOLDER = "data" + "/" + label.lower()

    st.spinner("Pushing files to dataset repo")

    api.upload_folder(
        folder_path=WAVE_OUTPUT_FOLDER,
        path_in_repo=REPO_FOLDER,
        repo_id=st.session_state['hugging_face_repo'],
        repo_type="dataset",
    )

    files = [WAVE_OUTPUT_FOLDER + f for f in os.listdir(WAVE_OUTPUT_FOLDER) if os.path.isfile(os.path.join(WAVE_OUTPUT_FOLDER, f))]
    for f in files:
        os.remove(f)


def download_dataset() -> None:
    folder_path = snapshot_download(st.session_state['hugging_face_repo'], repo_type="dataset")
    st.session_state['dataset_folder'] = folder_path + "/data"


def visualize_audio() -> None:
    data = load_data_info()
    try:
        folder_path = st.session_state['dataset_folder'] + "/" + st.session_state['label_name'].lower()

        cols = st.columns([2, 8, 2, 2])
        with cols[0]:
            st.write("File name")
        with cols[1]:
            st.write("Audio")
        with cols[2]:
            st.write("Date")
        with cols[3]:
            st.write("User Name")

        for f in os.listdir(folder_path):
            audio_path = folder_path + "/" + f
            audio_data, sampling_rate = sf.read(audio_path)

            temp_audio_path = "temp_audio.wav"
            sf.write(temp_audio_path, audio_data, sampling_rate)
            
            audio_name = audio_path.split("/")[-1]
            file_id = re.sub(r"([a-zA-Z]+)-([a-zA-Z0-9]+).wav", r"\2", audio_name)

            row = data[data['file_id'] == file_id]

            cols = st.columns([2, 8, 2, 2])
            with cols[0]:
                try:
                    st.markdown(f"[{audio_name}]({row.hugging_face_link.iloc[0]})")
                except:
                    st.write(f"{audio_name}")
            with cols[1]:
                st.audio(temp_audio_path, format="audio/wav", start_time=0)
            with cols[2]:
                try:
                    st.write(row.date.iloc[0])
                except:
                    st.write("No date information")
            with cols[3]:
                try:
                    st.write(row.user_name.iloc[0])
                except:
                    st.write("No user IP information")

            os.remove(temp_audio_path)
    except:
        st.write("No audio files in this label")

def load_data_info():
    return pd.read_csv(st.session_state['dataset_folder'] + "/data.csv")


def add_data_info(new_data_tab):
    df = load_data_info()

    new_rows = []
    for i in range(len(new_data_tab)):
        new_row = {
            'file_id': new_data_tab[i]['file_id'],
            'label': new_data_tab[i]['label'].lower().replace(" ", "_"),
            'user_name': new_data_tab[i]['user_name'].lower().replace(" ", "_"),
            'date': new_data_tab[i]['date'], 
            'timestamp': new_data_tab[i]['timestamp'], 
            'filename': new_data_tab[i]['filename'],
            'user_ip': new_data_tab[i]['user_ip'], 
            'is_in_dataset': True,
            'hugging_face_link': new_data_tab[i]['hugging_face_link'] 
        }
        new_rows.append(new_row)

    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    df.to_csv('data.csv', index=False)

    api = HfApi()
    api.upload_file(
        path_or_fileobj="data.csv",
        path_in_repo="data/data.csv",
        repo_id=st.session_state['hugging_face_repo'],
        repo_type="dataset",
    )

    os.remove("data.csv")

def clear_data_info():
    df = pd.DataFrame(columns=['file_id', 'label', 'user_name', 'date', 'timestamp', 'filename', 'user_ip', 'is_in_dataset', 'hugging_face_link'])
    df.to_csv('data.csv', index=False)

    api = HfApi()
    api.upload_file(
        path_or_fileobj="data.csv",
        path_in_repo="data/data.csv",
        repo_id=st.session_state['hugging_face_repo'],
        repo_type="dataset",
    )

    os.remove("data.csv")

def init_data_info():
    df = pd.DataFrame(columns=['file_id', 'label', 'user_name', 'date', 'timestamp', 'filename', 'user_ip', 'is_in_dataset', 'hugging_face_link'])
    df.to_csv('data.csv', index=False)

    api = HfApi()
    api.upload_file(
        path_or_fileobj="data.csv",
        path_in_repo="data/data.csv",
        repo_id="PFEE-TxE/audio_sampler",
        repo_type="dataset",
    )

    os.remove("data.csv")

if __name__ == "__main__":
    init_data_info()