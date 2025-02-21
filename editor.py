
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx import resize
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Load the video clip
video_clip = VideoFileClip("clean-4k.mp4")

# Create a TextClip with the text "deez" using Proxima Nova font
font = "Proxima-Nova-Bold"
text_clip = TextClip("deez", fontsize=50, color='white', font=font)

# Make the text clip the same duration as the video
text_clip = text_clip.set_duration(video_clip.duration)
text_clip = text_clip.set_position("center")

# Overlay the text on top of the video
video_with_text = CompositeVideoClip([video_clip, text_clip])
# Write the final video with text to a file
video_with_text.write_videofile("output.mp4", codec="libx264", fps=video_clip.fps, threads=8)