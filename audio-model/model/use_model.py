import numpy as np
import torch
import torch.nn as nn
import soundfile as sf

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, Wav2Vec2FeatureExtractor

from model.wav_to_vec import CustomWav2Vec2ForClassification

def load_model():
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").wav2vec2
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")

    num_labels = 4
    model.classifier = nn.Linear(model.config.hidden_size, num_labels)
    model.config.problem_type = "single_label_classification"

    model = CustomWav2Vec2ForClassification(model, model.classifier,num_labels)

    state_dict_path = "../models/model_v1_13_01.pth"
    model.load_state_dict(torch.load(state_dict_path, map_location=torch.device('cpu')))

    return model

def predict_single_audio_from_file(model, audio_file_path):

    device = "cpu"
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")

    speech, sample_rate = sf.read(audio_file_path)

    input_values = feature_extractor(speech, sampling_rate=sample_rate, return_tensors="pt").input_values

    model = model.to(device)
    input_values = input_values.to(device)

    with torch.no_grad():
        model_output = model(input_values)
        logits = model_output['logits']

    predicted_label_idx = np.argmax(logits.cpu().numpy(), axis=-1)



    return predicted_label_idx[0], logits.cpu().numpy()

# Example usage
# audio_file_path = "Sapin-01408dc1.wav"  # Replace with the path to your .wav file
# predicted_label_idx = predict_single_audio_from_file(audio_file_path)

# print(f"Predicted label index: {predicted_label_idx}")




