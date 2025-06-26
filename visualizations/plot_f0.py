import matplotlib.pyplot as plt
def plot_f0_curve(f0_ref, f0_synth, name='Sample', nameis='Sample2'):
    plt.figure(figsize=(10,4))
    plt.plot(f0_ref, label='Reference F0', color='blue')
    plt.plot(f0_synth, label='Synthesis F0', color='red', alpha=0.7)
    plt.title(f"F0 Contour Comparison - {name}")
    plt.xlabel("Frames")
    plt.ylabel("Pitch (Hz)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{name} -> {nameis}")
    plt.show()
