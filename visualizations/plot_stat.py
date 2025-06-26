import matplotlib.pyplot as plt
import numpy as np

def plot_stat_moments(mean_ref, std_ref, kurtosis_ref, mean_synth, std_synth, kurtosis_synth, name='Sample', nameis='Sample2'):
    metrics = ['Mean', 'STD', 'Kurtosis']
    stat_ref = [mean_ref, std_ref, kurtosis_ref]
    stat_synth = [mean_synth, std_synth, kurtosis_synth]
    x = np.arange(len(metrics))
    width = 0.35
    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width/2, stat_ref, width, label='Reference', color='skyblue')
    bars2 = ax.bar(x + width/2, stat_synth, width, label='Synthesized', color='salmon')
    ax.set_ylabel('Value')
    ax.set_title(f'Statistical Moments - {name} -> {nameis}')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f"STAT - {name} -> {nameis}")
    plt.show()
