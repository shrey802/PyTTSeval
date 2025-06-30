# A spectrogram is like a visual fingerprint of sound.
# MSD measures the difference between the mel spectrograms of a reference and a synthesized audio signal — frame by frame.


import numpy as np
import librosa
from pathlib import Path
import matplotlib.pyplot as plt

def extract_melspectogram(path, sr=22050):
    y, _ = librosa.load(path, sr=sr)
    melspec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft = 2048, hop_length = 512, n_mels = 90)
    return melspec

def compute_msd(ref_spec, synth_spec):
    min_len = min(ref_spec.shape[1], synth_spec.shape[1])
    mel_ref = ref_spec[:, :min_len]
    mel_synth = synth_spec[:, :min_len]
    mel_ref_db = librosa.power_to_db(mel_ref)
    mel_synth_db = librosa.power_to_db(mel_synth)
    diff = mel_ref_db - mel_synth_db
    dist = np.sqrt(np.mean(diff ** 2)) 
    return dist, diff

def run_msd(ref_dir, synth_dir):
    ref_paths = sorted(Path(ref_dir).glob("*.wav"))
    synth_paths = sorted(Path(synth_dir).glob("*.wav"))
    results = []
    for i, (ref_file, synth_file) in enumerate(zip(ref_paths, synth_paths)):
        print(f"\nPair {i+1}:")
        print(f"REF: {ref_file.name}")
        print(f"SYNTH: {synth_file.name}")
        try:
            mfcc_ref = extract_melspectogram(ref_file)
            mfcc_synth = extract_melspectogram(synth_file)
            msd,diff = compute_msd(mfcc_ref, mfcc_synth)
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(diff, sr=22050, x_axis='time', y_axis='mel', cmap='coolwarm')
            plt.title(f"MSD Diff Spectrogram: {ref_file.name} vs {synth_file.name}")
            plt.colorbar(label='dB Difference')
            plt.tight_layout()
            plt.savefig(f"MSD_{ref_file.stem}_{synth_file.stem}.png")
            plt.show()
            print(f"MSD: {msd:.2f} dB")
            results.append((ref_file.name, synth_file.name, msd))
        except Exception as e:
            print(f"Error computing MCD for {ref_file.name}: {e}")
            results.append((ref_file.name, synth_file.name, None))
    return results