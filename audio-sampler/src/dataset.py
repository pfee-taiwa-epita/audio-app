import pandas as pd
import os
import streamlit as st
import soundfile as sf
import re

from src.dataloader import load_data

from huggingface_hub import HfApi

def download_dataset(download=False) -> None:
    return load_data(download)

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

def visualize_audio() -> None:
    data = st.session_state['data']
    if (st.session_state['user_name_visu'] != []):
        data = data[data['user_name'].isin([x.lower().replace(" ", "_") for x in st.session_state['user_name_visu']])]

    if (st.session_state['label_name_visu'] != []):
        data = data[data['label'].isin([x.lower() for x in st.session_state['label_name_visu']])]

    data = data.sort_values(by=['timestamp'])

    st.subheader(f"{len(data)} audio files")

    cols = st.columns([2, 8, 2, 2])
    with cols[0]:
        st.write("File name")
    with cols[1]:
        st.write("Audio")
    with cols[2]:
        st.write("User Name")
    with cols[3]:
        st.write("Date")

    for index, row in data.iterrows():
        cols = st.columns([2, 8, 2, 2])
        with cols[0]:
            st.markdown(f"[{row.filename}]({row.hugging_face_link})")
        with cols[1]:
            st.audio(row.file_path, format="audio/wav", start_time=0)
        with cols[2]:
            st.text_input(value=row.user_name.replace("_", " ").title(), disabled=True, label=f"user_name{index}", label_visibility="collapsed")
        with cols[3]:
            st.text_input(value=row.date, disabled=True, label=f"date{index}", label_visibility="collapsed")

def add_data_info(new_data_tab):
    df = pd.read_csv(st.session_state['dataset_folder'] + "/data/data.csv", sep=",")

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