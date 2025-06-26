from utils.prepare_data import input_zip
from metrics.f0 import run_f0_fe_batch
from metrics.stat_moment import run_stat_moment

# Metrics Paths
ref_path = "/home/shreyash/Desktop/PyTTSeval/data/GoogleTTS/reference"
synth_path = "/home/shreyash/Desktop/PyTTSeval/data/GoogleTTS/synthesis"


def main():
    print("TTS Evaluation data preparation step")
    # input_zip()

# F0 results
# results = run_f0_fe_batch(ref_path, synth_path)

# Stat moments
# result_stat_moment = run_stat_moment(ref_path, synth_path)

if __name__ == "__main__":
    main()
