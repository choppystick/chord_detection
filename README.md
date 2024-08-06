# Chord Detection Project

This project performs audio analysis and visualization, focusing on note recognition as a step towards chord detection. It utilizes Fast Fourier Transform (FFT) and chromagram techniques to analyze audio files and create visualizations.

## Features

1. Waveform and Chromagram Visualization
2. Real-time Short-Time Fourier Transform (STFT) Animation
3. Peak Frequency Detection and Note Recognition
4. Audio-Video Synchronization

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- Librosa
- MoviePy

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/chord-detection-project.git
   cd chord-detection-project
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place your audio file (WAV format) in the project directory.

2. Update the `file_path` variable in `main.py` with your audio file name:
   ```python
   file_path = "your_audio_file.wav"
   ```

3. Run the script:
   ```
   python main.py
   ```

4. The script will generate:
   - A static plot showing the waveform and chromagram
   - An animated video of the STFT analysis
   - A final video with the STFT animation synchronized with the original audio

## Future Development

This project is currently in the note recognition phase. Future developments will focus on implementing chord detection algorithms based on the recognized notes.

Some features to add:
- Better file-handling
- Chord recognition
- Improve this readme
## License

This project is licensed under the MIT License.


## Acknowledgments

This project uses the following libraries:
- Librosa for audio analysis
- Matplotlib for plotting and animation
- MoviePy for video editing

References:
1) "Design and Evaluation of a Simple Chord Detection Algorithm" by Christoph Hausner: http://www.fim.uni-passau.de/fileadmin/files/lehrstuhl/sauer/geyer/BA_MA_Arbeiten/BA-HausnerChristoph-201409.pdf


