import pandas as pd
import os
import glob
from huggingface_hub import snapshot_download, HfApi, HfFolder

from folder_path import DATASET_FOLDER, AUGMENTED_DATASET_FOLDER

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

def download_augmented_data():
    os.system(f"rm -rf {AUGMENTED_DATASET_FOLDER}/*") 
    snapshot_download("PFEE-TxE/data_augmented", repo_type="dataset", local_dir=AUGMENTED_DATASET_FOLDER)

def extract_info_corrected_v2(file_name):
    # remove everything before the last /
    file_path = file_name
    file_name = file_name.split('/')[-1]

    base_name = file_name[:-4]
    parts = base_name.split('_')

    pitch = 0
    noise = None
    origin = parts[0]
    label = origin.split('-')[0].lower()

    for i in range(len(parts)):
        if parts[i] == 'minus':
            pitch = -1 * int(parts[i + 1])
        elif parts[i] == 'plus':
            pitch = int(parts[i + 1])

    if not (len(parts) == 1 or len(parts) == 3):
        noise = parts[-1]
    
    return origin, label, pitch, noise, file_name, file_path,

def load_augmented_data(download=False):
    if download:
        download_augmented_data()

    list_str = glob.glob(os.path.join(AUGMENTED_DATASET_FOLDER, '*'))
    
    df = pd.DataFrame([extract_info_corrected_v2(file) for file in list_str], 
                               columns=['origin_file', 'label', 'pitch', 'noise', 'file_name', 'file_path'])

    return df

# def push_to_huggingface():
#     api = HfApi()

#     api.upload_folder(
#         folder_path=AUGMENTED_DATASET_FOLDER,
#         repo_id="PFEE-TxE/data_augmented",
#         repo_type="dataset",
#     )