from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize

# Define the input video file path
input_video_file = "./output/manymanycheating.mp4"

# Define the output video file path
output_video_file = "./output/cropped_manymanycheating.mp4"

# Define the desired vertical aspect ratio (e.g., 9:16)
vertical_aspect_ratio = (9, 16)

# Define the duration (in seconds) you want to keep

# Load the input video clip
video_clip = VideoFileClip(input_video_file)
duration_to_keep = min(video_clip.duration, 58)


# Calculate the target width based on the vertical aspect ratio
target_width = int(video_clip.h * (vertical_aspect_ratio[0] / vertical_aspect_ratio[1]))

# Calculate the y-coordinate to center the cropped area
x_center = (video_clip.w - target_width) // 2 

# Crop the video to the desired aspect ratio (centered)
cropped_clip = crop(video_clip, x1=x_center, x2=x_center + target_width)

# Trim the video to the desired duration
final_clip = cropped_clip.subclip(0, duration_to_keep)

upscaled_clip = resize(final_clip, width=1080, height=1920)

# Write the final video to the output file
upscaled_clip.write_videofile(output_video_file,  codec='mpeg4')

# Close the video clips
video_clip.close()
final_clip.close()

print(f"Video cropped and trimmed to {duration_to_keep} seconds with a vertical aspect ratio. Saved as {output_video_file}")