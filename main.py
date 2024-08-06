import numpy as np
import matplotlib.pyplot as plt
import librosa.feature
import librosa.display
from matplotlib.animation import FuncAnimation
from moviepy.editor import VideoFileClip, AudioFileClip


def analyze_wav(file_path):
    # Load the audio file using librosa
    audio_data, sample_rate = librosa.load(file_path, sr=None)

    # Calculate time array
    time = np.linspace(0, len(audio_data) / sample_rate, num=len(audio_data))

    # Compute chromagram
    hop_length = 512
    n_fft = 2048
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)

    # Plot waveform
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time, audio_data)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Plot chromagram with pitch classes as axis
    plt.subplot(2, 1, 2)
    librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', sr=sample_rate, hop_length=hop_length)
    # librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),y_axis='log', x_axis='time', sr=sample_rate,
    # hop_length=hop_length)
    plt.title('Chromagram')
    plt.xlabel('Time (s)')
    plt.colorbar(label='Magnitude')

    plt.tight_layout()
    plt.show()


def hz_to_note(freq):
    A4 = 440
    C0 = A4 * pow(2, -4.75)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    if freq == 0:
        return "N/A"

    h = round(12 * np.log2(freq / C0))
    octave = h // 12
    n = h % 12
    return note_names[n] + str(octave)


def create_stft_animation(file_path, output_path, num_peaks=3, max_freq=None):
    # Load the audio file
    audio_data, sample_rate = librosa.load(file_path, sr=None)

    # Set up STFT parameters
    n_fft = 2048
    hop_length = 512

    # Compute STFT
    stft = librosa.stft(audio_data, n_fft=n_fft, hop_length=hop_length)

    # Convert to magnitude
    mag = np.abs(stft)

    # Frequency array for x-axis
    freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=n_fft)

    # Find the index of the frequency closest to max_freq (if specified)
    if max_freq is not None:
        freq_limit_index = np.argmin(np.abs(freqs - max_freq))
    else:
        freq_limit_index = len(freqs)

    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate the duration of each frame
    frame_duration = hop_length / sample_rate

    # Animation function
    def animate(frame, mag=mag):
        ax.clear()

        frame_mag = mag[:freq_limit_index, frame]

        # Plot the frequency spectrum
        ax.plot(freqs[:freq_limit_index], frame_mag, lw=2)

        # Set axis limits
        ax.set_xlim(0, freqs[freq_limit_index - 1])
        ax.set_ylim(0, np.max(mag[:freq_limit_index]) * 1.1)

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude')
        ax.set_title(f'Short-Time Fourier Transform - Time: {frame * frame_duration:.2f}s')

        # Find the top N peak frequencies
        peak_indices = np.argsort(frame_mag)[-num_peaks:][::-1]
        peak_freqs = freqs[peak_indices]
        peak_mags = frame_mag[peak_indices]
        peak_notes = [hz_to_note(freq) for freq in peak_freqs]

        # Add points and labels for the peaks
        for i, (freq, mag, note) in enumerate(zip(peak_freqs, peak_mags, peak_notes)):
            ax.plot(freq, mag, 'ro')
            ax.annotate(f'{freq:.1f}Hz ({note})',
                        (freq, mag),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="b", lw=1, alpha=0.8))

        return ax.lines + ax.texts

    # Create animation
    anim = FuncAnimation(fig, animate, frames=mag.shape[1], interval=int(frame_duration * 1000), blit=False)

    # Save the animation as an MP4 file
    anim.save(output_path, writer='ffmpeg', fps=int(1 / frame_duration))

    plt.close(fig)


def add_audio_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    video = video.set_audio(audio)
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')


file_path = "sample2.wav"
video_output = 'stft_animation.mp4'
final_output = 'stft_animation_with_audio.mp4'

analyze_wav(file_path)
create_stft_animation(file_path, video_output, max_freq=5000)

# Add audio to the video
add_audio_to_video(video_output, file_path, final_output)
