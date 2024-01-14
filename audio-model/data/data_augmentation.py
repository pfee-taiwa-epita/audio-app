import random
import os
import shutil

from pydub import AudioSegment
from tqdm import tqdm

from folder_path import AUGMENTED_DATASET_FOLDER, DATASET_FOLDER, NOISE_FOLDER

def convert_mp3_to_wav(filename: str):

    sound = AudioSegment.from_mp3(filename)
    filename = filename[:-4]
    sound.export(filename + '.wav', format="wav")

def copy_data_to_augmented_dataset():
    source_dir = DATASET_FOLDER
    dest_dir = AUGMENTED_DATASET_FOLDER

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)

    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)

        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                shutil.copy(file_path, dest_dir)

def merge_audio_with_noise(record_file: str, noise_file: str, noise_name: str):
    original = AudioSegment.from_file(record_file)
    background_noise = AudioSegment.from_file(noise_file) - 30

    background_duration = len(background_noise)

    start_point = random.randint(0, background_duration - 2000)
    selected_noise = background_noise[start_point:start_point + 2000]

    combined = original.overlay(selected_noise)

    new_file_name = record_file[:-4] + '_' + noise_name + ".wav"

    combined.export(new_file_name, format='wav')

def pitch_shift(audio_file, semitones):
    song = AudioSegment.from_file(audio_file, format="wav")
    shifted_song = song._spawn(song.raw_data, overrides={
        "frame_rate": int(song.frame_rate * (2 ** (semitones / 12.0)))
    }).set_frame_rate(song.frame_rate)

    sign = 'plus' if semitones >= 0 else 'minus'
    
    new_file_name = audio_file[:-4] + "_" + sign + "_" + str(abs(semitones)) + ".wav"

    shifted_song.export(new_file_name, format="wav")


def generate_augmented_dataset(semitones: [int], noises: [str]) -> None:
    copy_data_to_augmented_dataset()
    folder = AUGMENTED_DATASET_FOLDER

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            for semitone in semitones:
                pitch_shift(AUGMENTED_DATASET_FOLDER + '/' + file, semitone)

    for file in tqdm(os.listdir(folder), desc="Processing Files"):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            for noise in noises:
                merge_audio_with_noise(AUGMENTED_DATASET_FOLDER + '/' + file, NOISE_FOLDER + '/' + noise + '.wav', noise)


def create_augmented_dataset(semitones: [int], noises: [str]) -> None:

    generate_augmented_dataset(semitones, noises)

