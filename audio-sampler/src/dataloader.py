import pandas as pd
import streamlit as st
import os
from huggingface_hub import snapshot_download


def download_data():
    DATASET_FOLDER = st.session_state['dataset_folder']
    os.system(f"rm -rf {DATASET_FOLDER}/*") 
    snapshot_download("PFEE-TxE/audio_sampler", repo_type="dataset", local_dir=DATASET_FOLDER)

def check_file_in_csv():
    DATASET_FOLDER = st.session_state['dataset_folder']
    df = pd.read_csv(DATASET_FOLDER + "/data/data.csv", sep=",")
    for index, row in df.iterrows():
        label = row["label"]
        filename = row["filename"]
        if os.path.isfile(f"{DATASET_FOLDER}/data/{label}/{filename}"):
            df.loc[index, "is_in_dataset"] = True
        else:
            df.loc[index, "is_in_dataset"] = False

    df.to_csv(DATASET_FOLDER + "/data/data.csv", sep=",", index=False)

def load_data(download=False):
    DATASET_FOLDER = st.session_state['dataset_folder']
    if download:
        download_data()
    else:
        if len(os.listdir(DATASET_FOLDER + "/data")) == 0:
            download_data()

    check_file_in_csv()
    
    df = pd.read_csv(DATASET_FOLDER + "/data/data.csv", sep=",")
    df = df[df["is_in_dataset"] == True]
    df["file_path"] = DATASET_FOLDER + "/data/" + df["label"] + "/" + df["filename"]
    df = df.drop(columns=["file_id", "user_ip", "is_in_dataset"])

    st.session_state['data'] = df

def button_refresh_data():
    if st.button("Refresh data 🔄"):
        load_data(True)