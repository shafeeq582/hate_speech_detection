# hate_speech_beeper

import librosa
import numpy as np
import soundfile as sf
import torch
import transformers
from sklearn.ensemble import IsolationForest
from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Suppress warnings
transformers.logging.set_verbosity_error()

# Load Wav2Vec 2.0 model for feature extraction
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h", ignore_mismatched_sizes=True)

def extract_features(audio_file):
    audio, sr = librosa.load(audio_file, sr=16000)
    inputs = processor(audio, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        features = model(inputs).last_hidden_state.squeeze(0).numpy()
    return features, sr, audio

def detect_hate_speech(features):
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(features)
    return clf.predict(features)

def beep_hate_speech(audio, sr, predictions, beep_freq=1000, beep_duration=0.2):
    step_size = len(audio) // len(predictions)
    beep = np.sin(2 * np.pi * np.arange(int(beep_duration * sr)) * beep_freq / sr)
    
    for i, pred in enumerate(predictions):
        if pred == -1:
            start = i * step_size
            end = min((i + 1) * step_size, len(audio))
            beep_resized = np.resize(beep, end - start)
            audio[start:end] = beep_resized
    return audio

def process_audio(input_audio, output_audio):
    print(f"Processing audio for hate speech beeping...")
    features, sr, audio = extract_features(input_audio)
    predictions = detect_hate_speech(features)
    modified_audio = beep_hate_speech(audio, sr, predictions)
    sf.write(output_audio, modified_audio, sr)
    print(f"Beeped audio saved to: {output_audio}")
