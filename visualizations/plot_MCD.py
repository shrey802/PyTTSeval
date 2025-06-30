import matplotlib.pyplot as plt
import librosa.display

def plot_mcd(ref_path, synth_path, name='Sample', nameis='Sample2'):
    y1, _ = librosa.load(ref_path)
    y2, _ = librosa.load(synth_path)

    plt.figure(figsize=(12, 3))
    plt.title("Waveform Comparison")
    librosa.display.waveshow(y1, alpha=0.6, label="Reference")
    librosa.display.waveshow(y2, alpha=0.6, color='orange', label="Synth")
    plt.legend()
    plt.savefig(f"MCD -> {name} -> {nameis}")
    plt.show()