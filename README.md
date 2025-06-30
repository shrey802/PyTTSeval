
# PyTTSeval v1.0

Implemented 5 key objective metrics in version 1 of this project for evaluating TTS systems' outputs. 

Each metric compares a synthetic audio sample to a reference (real) audio sample, assessing aspects such as pitch accuracy, spectral similarity, and statistical features with accompanying visualization. 

## List of Metrics :
1) DTW (Dynamic Time Wrapping)
2) MCD (Mel Cepstral Distortion)
3) MSD (Mel Spectral Distortion)
4) F0 Frame Error
5) Stat Moments (Kurtosis, Mean, STD)


## Setup

1) Create a new conda environment
2) Take reference audio and generate synthesis using any open source TTS (I've used LJSpeech as reference and Kokoro TTS for synthesis)
3) Create a folder and inside that create 2 folders with these names (synthesis, reference)
4) Put all your audio files in their respective folders
5) Zip the folder and add it to the root folder
6) Run main.py and give the path of the zip file and where you want to extract
7) Keep uncommenting all the functions one by one and save all the metrics visualizations

## Future Version Ideas

1) More metrics
2) ASR (phoneme matching) for multiple languages
