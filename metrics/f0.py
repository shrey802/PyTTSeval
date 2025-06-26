# Fundamental Frequency is basically nothing but first pattern in a waveform and then same pattern repeats throught the same waveform. So if the frame repeats every 100ms then it has 100Hz.It's called pitch 
# Absolute diff between ref - synth / ref (why divide coz if we don't a 10Hz error occurs and it will matter in some waveforms)

import librosa
import numpy as np
from pathlib import Path
from visualizations.plot_f0 import plot_f0_curve

# we extract fundamental frequency using yin algorithm
def extract_f0(path, sr=22050, fmin=50, fmax=500):
    y, _ = librosa.load(path, sr=sr)
    f0,_, _ = librosa.pyin(y, fmin=fmin, fmax=fmax, hop_length=256, sr=sr, frame_length=1024)
    return f0

# rmse and percent error using their math formulas
def compute_f0_frame_error(f0_ref, f0_synth):

    min_len = min(len(f0_ref), len(f0_synth))
    f0_ref = f0_ref[:min_len]
    f0_synth = f0_synth[:min_len]

    mask = ~np.isnan(f0_ref) & ~np.isnan(f0_synth)

    if np.sum(mask) == 0:
        raise ValueError("No overlapping voiced frames.")

    f0_ref_voiced = f0_ref[mask]
    f0_synth_voiced = f0_synth[mask]

    percent_error = np.mean(np.abs(f0_ref_voiced - f0_synth_voiced) / f0_ref_voiced) * 100
    rmse_error = np.sqrt(np.mean((f0_ref_voiced - f0_synth_voiced) ** 2))

    return percent_error, rmse_error


# main function to call other functions
def run_f0_fe_batch(ref_folder, synth_folder):
    ref_paths = sorted(Path(ref_folder).glob("*.wav"))
    synth_paths = sorted(Path(synth_folder).glob("*.wav"))
    if len(ref_paths) != len(synth_paths):
        raise ValueError("Mismatch: reference and synthesized folders must contain same number of files.")
    results = []
    for i, (ref_file, synth_file) in enumerate(zip(ref_paths, synth_paths)):
        print(f"\nPair {i+1}:")
        print(f"REF: {ref_file.name}")
        print(f"SYNTH: {synth_file.name}")
        try:
            f0_ref = extract_f0(ref_file)
            f0_synth = extract_f0(synth_file)
            plot_f0_curve(f0_ref, f0_synth, name=ref_file.stem, nameis=synth_file.stem)
            percent_error, rmse_error = compute_f0_frame_error(f0_ref, f0_synth)
            print(f"F0-FE: {percent_error:.2f}% | RMSE: {rmse_error:.2f} Hz")
            results.append({
                "ref_file": ref_file.name,
                "synth_file": synth_file.name,
                "percent_error": percent_error,
                "rmse": rmse_error
            })
        except Exception as e:
            print(f"Error: {e}")
            results.append({
                "ref_file": ref_file.name,
                "synth_file": synth_file.name,
                "percent_error": None,
                "rmse": None,
                "error": str(e)
            })
    return results