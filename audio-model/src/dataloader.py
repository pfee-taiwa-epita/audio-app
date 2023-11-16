import pandas as pd
import os
from huggingface_hub import snapshot_download

DATASET_FOLDER = "../dataset"

def download_data():
    os.system(f"rm -rf {DATASET_FOLDER}/*") 
    snapshot_download("PFEE-TxE/audio_sampler", repo_type="dataset", local_dir=DATASET_FOLDER)

def check_file_in_csv():
    df = pd.read_csv(DATASET_FOLDER + "/data/data.csv", sep=",")
    for index, row in df.iterrows():
        label = row["label"]
        filename = row["filename"]
        if os.path.isfile(f"{DATASET_FOLDER}/data/{label}/{filename}"):
            df.loc[index, "is_in_dataset"] = True
        else:
            df.loc[index, "is_in_dataset"] = False

    df.to_csv(DATASET_FOLDER + "/data/data.csv", sep=",", index=False)


'''
     label  user_name                 date                                     file_path
0  bouleau  stanley_s  2023-11-09 11:21:39  ../dataset/data/bouleau/Bouleau-dc09357b.wav
1  bouleau  stanley_s  2023-11-09 11:22:10  ../dataset/data/bouleau/Bouleau-a0dde262.wav
2  bouleau  stanley_s  2023-11-09 11:22:12  ../dataset/data/bouleau/Bouleau-e6cac553.wav
3  bouleau  stanley_s  2023-11-09 11:22:15  ../dataset/data/bouleau/Bouleau-6f8a158a.wav
4  bouleau  stanley_s  2023-11-09 11:22:17  ../dataset/data/bouleau/Bouleau-cf0dc1d7.wav
'''
def load_data(download=False):
    if download:
        download_data()

    check_file_in_csv()
    
    df = pd.read_csv(DATASET_FOLDER + "/data/data.csv", sep=",")
    df = df[df["is_in_dataset"] == True]
    df["file_path"] = DATASET_FOLDER + "/data/" + df["label"] + "/" + df["filename"]
    df = df.drop(columns=["file_id", "timestamp", "user_ip", "hugging_face_link", "is_in_dataset", "filename"])

    return df