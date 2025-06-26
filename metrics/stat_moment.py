# Mean (μ)
#    The average pitch over time.
#    Higher mean = generally higher-pitched voice.
#    Example: A speaker with consistent 200 Hz pitch → Mean ≈ 200 Hz

# Standard Deviation (σ)
#    Measures how much the pitch varies from the mean.
#    - High STD: pitch rises and falls → expressive, emotional speech
#    - Low STD: pitch stays near the mean → flat, robotic tone

# Kurtosis
#    Describes the sharpness or "peakedness" of pitch values.
#    - High kurtosis: sharp spikes in pitch → possibly unnatural or overemphasized
#    - Low kurtosis: flatter curve → smooth or dull speech



import librosa
import numpy as np
from pathlib import Path
from scipy.stats import kurtosis
from visualizations.plot_stat import plot_stat_moments

# we extract fundamental frequency using yin algorithm
def extract_f0(path, sr=22050, fmin=50, fmax=500):
    y, _ = librosa.load(path, sr=sr)
    f0, _, _ = librosa.pyin(y, fmax=fmax, fmin=fmin, sr=sr, hop_length=256, frame_length=1024)
    return f0

def run_stat_moment(ref_folder, synth_folder):
    ref_paths = sorted(Path(ref_folder).glob("*.wav"))
    synth_paths = sorted(Path(synth_folder).glob("*.wav"))
    
    for i, (ref_file, synth_file) in enumerate(zip(ref_paths, synth_paths)):
        print(f"\n📁 Pair {i+1}:")
        print(f"REF: {ref_file.name}")
        print(f"SYNTH: {synth_file.name}")
        try:
            f0_ref = extract_f0(ref_file)
            f0_synth = extract_f0(synth_file)
            f0_ref_clean = f0_ref[~np.isnan(f0_ref)]
            f0_synth_clean = f0_synth[~np.isnan(f0_synth)]

            # reference stat moments
            mean_ref = np.mean(f0_ref_clean)
            std_ref = np.std(f0_ref_clean)
            kurtosis_ref = kurtosis(f0_ref_clean)

            # synthesis stat moments
            mean_synth = np.mean(f0_synth_clean)
            std_synth = np.std(f0_synth_clean)
            kurtosis_synth = kurtosis(f0_synth_clean)
            plot_stat_moments(mean_ref, std_ref, kurtosis_ref, mean_synth, std_synth, kurtosis_synth, name=ref_file.stem, nameis=synth_file.stem)
            print(f"Reference  → Mean: {mean_ref:.2f} Hz | STD: {std_ref:.2f} | Kurtosis: {kurtosis_ref:.2f}")
            print(f"Synthesized → Mean: {mean_synth:.2f} Hz | STD: {std_synth:.2f} | Kurtosis: {kurtosis_synth:.2f}")
        except Exception as e:
            print(f"Error: {e}")