from utils.prepare_data import input_zip
from metrics.f0 import run_f0_fe_batch
def main():
    print("TTS Evaluation data preparation step")
    # input_zip()


ref_path = "/home/shreyash/Desktop/PyTTSeval/data/Kokoro/reference"
synth_path = "/home/shreyash/Desktop/PyTTSeval/data/Kokoro/synthesis"

# F0 results
results = run_f0_fe_batch(ref_path, synth_path)


if __name__ == "__main__":
    main()
