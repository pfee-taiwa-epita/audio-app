import torch.nn as nn
from transformers import Wav2Vec2Config,Wav2Vec2ForCTC,Wav2Vec2Processor
import torch

class CustomWav2Vec2ForClassification(nn.Module):
    def __init__(self, wav2vec2_model, classifier,num_labels):
        super().__init__()
        self.wav2vec2 = wav2vec2_model
        self.classifier = classifier
        self.num_labels = num_labels

    def forward(self, input_values,labels=None):
        wav2vec2_outputs = self.wav2vec2(input_values=input_values)
        if isinstance(wav2vec2_outputs, torch.Tensor):
            outputs = wav2vec2_outputs
        else:
            outputs = wav2vec2_outputs.last_hidden_state

        outputs = outputs.mean(dim=1)  # Average pooling
        logits = self.classifier(outputs)

        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits, labels)

        return {"loss": loss, "logits": logits} if loss is not None else {"logits": logits}
