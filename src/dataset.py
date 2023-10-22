import os
import numpy as np
import streamlit as st
import soundfile as sf


from datasets import Dataset, Audio, load_dataset




def push_files_to_hub() -> None:
    WAVE_OUTPUT_FOLDER = st.session_state['wave_output_folder']

    files = [WAVE_OUTPUT_FOLDER + f for f in os.listdir(WAVE_OUTPUT_FOLDER) if os.path.isfile(os.path.join(WAVE_OUTPUT_FOLDER, f))]

    audio_dataset = Dataset.from_dict({"audio": files}).cast_column("audio", Audio())
    audio_dataset.push_to_hub("PFEE-TxE/audio_recorder")

    for f in files:
        os.remove(f)

def visualize_audio() -> None:
    dataset = load_dataset("PFEE-TxE/audio_recorder")
    for i in range(len(dataset['train'])):
        example = dataset['train'][i]
        audio_path = example['audio']['path']
        sampling_rate = example['audio']['sampling_rate']
        audio_data = np.array(example['audio']['array'])

        # Enregistrez les données audio temporairement en format WAV (vous pouvez aussi utiliser d'autres formats audio)
        temp_audio_path = "temp_audio.wav"
        sf.write(temp_audio_path, audio_data, sampling_rate)

        # Utilisez st.audio pour afficher le fichier audio
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{audio_path}")
        with col2:
            st.audio(temp_audio_path, format="audio/wav", start_time=0)

    os.remove(temp_audio_path)





