# DTW is an algorithm used to measure similarity between two 
# sequences that may vary in speed, length, or timing.

import numpy as np
import librosa
from pathlib import Path
import librosa.sequence
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import librosa.display

def extract_mfcc(path, sr=22050, n_mfcc=13):
    y, _ = librosa.load(path, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T  


def dtw(mfcc_ref, mfcc_synth):
    D, wp = librosa.sequence.dtw(X=mfcc_ref.T, Y=mfcc_synth.T, metric='euclidean')
    dtw_distance = D[-1, -1]  
    return dtw_distance, D, wp


def run_DTW(ref_dir, synth_dir):
    ref_paths = sorted(Path(ref_dir).glob("*.wav"))
    synth_paths = sorted(Path(synth_dir).glob("*.wav"))
    results = []
    for i, (ref_file, synth_file) in enumerate(zip(ref_paths, synth_paths)):
        print(f"\nPair {i+1}:")
        print(f"REF: {ref_file.name}")
        print(f"SYNTH: {synth_file.name}")
       
        try:
            mfcc_ref = extract_mfcc(ref_file)
            mfcc_synth = extract_mfcc(synth_file)
            dtw_dist, D, wp = dtw(mfcc_ref, mfcc_synth)
            plt.figure(figsize=(6, 6))
            librosa.display.specshow(D, x_axis='frames', y_axis='frames')
            plt.plot(wp[:, 1], wp[:, 0], marker='o', color='lime', label='Warp path')
            plt.title(f"DTW Alignment | {ref_file.name}")
            plt.xlabel("Synthesized")
            plt.ylabel("Reference")
            plt.colorbar(label='Distance')
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"DTW_{ref_file.stem}.png")
            plt.close()
            print(f"DTW: {dtw_dist:.2f}")
            results.append((ref_file.name, synth_file.name, dtw_dist))
        except Exception as e:
            print(f"Error computing DTW for {ref_file.name}: {e}")
            results.append((ref_file.name, synth_file.name, None))
    return results