# MFCC is nothing but a metric to evaluate the difference between two audio signals based on their spectral features — particularly their MFCCs (Mel-Frequency Cepstral Coefficients).
# It is often used to compare a synthesized voice to a reference natural voice.
# Lower MCD = closer the synthesized voice is to natural speech.
# Units: decibels (dB)

from pathlib import Path
import numpy as np
import librosa
from visualizations.plot_MCD import plot_mcd

def extract_mfcc(path, sr=22050, n_mfcc=13):
    y, _ = librosa.load(path, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T  

def compute_mcd(mfcc_ref, mfcc_synth):
    min_len = min(len(mfcc_ref), len(mfcc_synth))
    mfcc_ref = mfcc_ref[:min_len]
    mfcc_synth = mfcc_synth[:min_len]

    diff = mfcc_ref - mfcc_synth
    sq_diff = np.sum(diff ** 2, axis=1) 
    mcd = np.mean(np.sqrt(sq_diff)) * (10.0 / np.log(10)) * np.sqrt(2)

    return mcd

def run_mcd(ref_dir, synth_dir):
    ref_paths = sorted(Path(ref_dir).glob("*.wav"))
    synth_paths = sorted(Path(synth_dir).glob("*.wav"))
    results = []
    for i, (ref_file, synth_file) in enumerate(zip(ref_paths, synth_paths)):
        print(f"\nPair {i+1}:")
        print(f"REF: {ref_file.name}")
        print(f"SYNTH: {synth_file.name}")
        plot_mcd(ref_file, synth_file, name=ref_file.stem, nameis=synth_file.stem)
        try:
            mfcc_ref = extract_mfcc(ref_file)
            mfcc_synth = extract_mfcc(synth_file)
            mcd = compute_mcd(mfcc_ref, mfcc_synth)
            print(f"MCD: {mcd:.2f} dB")
            results.append((ref_file.name, synth_file.name, mcd))
        except Exception as e:
            print(f"Error computing MCD for {ref_file.name}: {e}")
            results.append((ref_file.name, synth_file.name, None))
    return results