import os
import requests
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# --- CONFIGURATION ---
REDDIT_POST_URL = "https://www.reddit.com/r/talesfromtechsupport/comments/1isi8ac/my_bank_account_isnt_working/.json"
VIDEO_INPUT = "input/1.mp4"
TEMP_AUDIO = "output/temp_audio.mp3"
FINAL_OUTPUT = "output/final_video.mp4"
MAX_AUDIO_LENGTH = 58  # seconds

# Ensure the output directory exists
os.makedirs("output", exist_ok=True)

# --- FETCH STORY FROM REDDIT ---
def get_reddit_story(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Reddit post: {response.status_code}")
    data = response.json()
    # Extract the post text (selftext)
    post_text = data[0]['data']['children'][0]['data'].get('selftext', '')
    return post_text

# --- GENERATE TTS AUDIO ---
def generate_tts(text, output_path):
    tts = gTTS(text)
    tts.save(output_path)
    return output_path

# --- TRIM AUDIO TO MAX LENGTH ---
def trim_audio(input_audio, max_length):
    audio_clip = AudioFileClip(input_audio)
    if audio_clip.duration > max_length:
        # Use with_duration to obtain a trimmed audio clip
        trimmed_audio = audio_clip.with_duration(max_length)
        # Overwrite the existing file with the trimmed audio
        trimmed_audio.write_audiofile(input_audio, codec='mp3')
    return input_audio

# --- CREATE VIDEO WITH AUDIO & SUBTITLES ---
def create_video_with_audio(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Determine the final duration (shorter of video and audio)
    final_duration = min(video.duration, audio.duration)
    # Use subclipped (the updated method) instead of subclip
    video = video.subclipped(0, final_duration)
    video = video.with_audio(audio)
    
    # For demonstration: create a simple subtitle using the first 100 words.
    # (For better results, you would split and sync subtitles properly.)
    subtitle_text = " ".join(get_reddit_story(REDDIT_POST_URL).split()[:100])
    txt_clip = TextClip(
        subtitle_text,
        color='white',
        size=(720, None),
        method='caption'
    )
    txt_clip = txt_clip.set_position('center').set_duration(final_duration)
    
    final_video = CompositeVideoClip([video, txt_clip])
    final_video.write_videofile(output_path, fps=30)

# --- MAIN SCRIPT ---
if __name__ == "__main__":
    print("Fetching Reddit story...")
    story_text = get_reddit_story(REDDIT_POST_URL)
    
    print("Generating TTS audio...")
    generate_tts(story_text, TEMP_AUDIO)
    
    print("Trimming audio if needed...")
    trim_audio(TEMP_AUDIO, MAX_AUDIO_LENGTH)
    
    print("Creating video with subtitles...")
    create_video_with_audio(VIDEO_INPUT, TEMP_AUDIO, FINAL_OUTPUT)
    
    print("Done! Video saved at:", FINAL_OUTPUT)
