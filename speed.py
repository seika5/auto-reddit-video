from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_file("./temp.mp3")

# Get the bitrate
bitrate = audio.frame_rate
print(f"Bitrate: {bitrate} bits per second")
sample_width = audio.sample_width

# Calculate the bit depth (in bits)
bit_depth = sample_width * 8

print(f"Bit depth: {bit_depth} bits")

audio_length_ms = len(audio)

# Convert milliseconds to a more human-readable format
audio_length_seconds = audio_length_ms / 1000

print(f"Audio length: {audio_length_seconds} seconds")