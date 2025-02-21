import pyttsx3
from pydub import AudioSegment
import re
import random

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips, ImageClip, VideoClip
from moviepy.audio.fx import volumex
from moviepy.video.fx.crop import crop
import tkinter as tk
import queue
import threading
from moviepy.video.fx.resize import resize

positions = []
engine = pyttsx3.init()
font = "Calibri-Bold"
outline_width = 5
max_width = 500
vertical_aspect_ratio = (9, 16)

def onWord(name, location, char, length):
    positions.append({
      "byte_location": location,
      "char_position": char,
      "word_length": length,
    })

engine.connect('started-word', onWord)
engine.setProperty('rate', 200)

def split_paragraph_into_words(paragraph):
    # Use regular expression to split the paragraph into words
    words = re.findall(r'\b\w+\b|[.,!?;]', paragraph)
    
    return words

def speak_string(speak_string):
    engine.say(speak_string, "temp.mp3")

    engine.runAndWait()
    engine.save_to_file(speak_string, "./output/temp.mp3")

    engine.runAndWait()
    tlen = positions[len(positions) - 1]["byte_location"]
    audio = AudioSegment.from_file("./output/temp.mp3")
    for x in positions:
        x["time_start"] = float(x["byte_location"]) / float(tlen) * (len(audio) / 1000 - (1))
        #print(speak_string[max(x["char_position"] - 1, 0):x["char_position"] + x["word_length"] + 1].strip(), x["time_start"])

def speak_title(title):
    engine.save_to_file(title, "./output/title.mp3")
    engine.runAndWait()

def crop_vertical(title):
    input_video_file = f"./output/{title}.mp4"
    output_video_file = f"./output/{title}_cropped.mp4"

    video_clip = VideoFileClip(input_video_file)
    duration_to_keep = min(video_clip.duration, 58)
    # target_width = int(video_clip.h * (vertical_aspect_ratio[0] / vertical_aspect_ratio[1]))
    # x_center = (video_clip.w - target_width) // 2
    # cropped_clip = crop(video_clip, x1=x_center, x2=x_center + target_width)

    #final_clip = cropped_clip.subclip(0, duration_to_keep)
    final_clip = video_clip.subclip(0, duration_to_keep)

    final_clip.write_videofile(output_video_file, codec="mpeg4", bitrate="24000k")
    video_clip.close()
    final_clip.close()

    print(f"Video cropped and trimmed to {duration_to_keep} seconds with a vertical aspect ratio. Saved as {output_video_file}")


def processOnePost(file_name, title, screenshot, text, minecraft_video="sesh2.mp4"):
    speak_title(title)
    speak_string(text)
    title_len = AudioSegment.from_file("./output/title.mp3")
    audio = AudioSegment.from_file("./output/temp.mp3")

        
    #Select random timestamp to begin
    total_video_duration = len(title_len) / 1000 + len(audio) / 1000 + 0.25
    video_clip = VideoFileClip(f"./input/{minecraft_video}")
    start_time = random.uniform(0, video_clip.duration - total_video_duration)
    video_clip = video_clip.subclip(start_time, start_time + total_video_duration)

    image_clip = ImageClip(f"./input/{screenshot}").set_position("center").set_duration(len(title_len) / 1000)
    width, height = image_clip.size
    new_width = min(width, max_width)
    new_height = int(height * (new_width / width))
    image_clip = image_clip.resize(width=new_width, height=new_height)

    text_clips = [image_clip]

    for x in range(len(positions)):
        mj = positions[x]
        text_clip = TextClip(text[max(mj["char_position"] - 1, 0):mj["char_position"] + mj["word_length"]].strip(), fontsize=100, color='white', font=font, stroke_width=2, stroke_color='black')
        text_clip = text_clip.set_duration(len(audio) / 1000 - float(mj["time_start"] - 0.5) if x + 1 == len(positions) else float(positions[x + 1]["time_start"] - positions[x]["time_start"]))
        text_clip = text_clip.set_position("center")

        text_clips.append(text_clip)

    positions.clear()
    final_clip = concatenate_videoclips(text_clips)
    final_clip = final_clip.set_position(("center"))

    video_with_text = CompositeVideoClip([video_clip, final_clip])

    target_width = int(video_with_text.h * (vertical_aspect_ratio[0] / vertical_aspect_ratio[1]))
    x_center = (video_with_text.w - target_width) // 2
    cropped_clip = crop(video_with_text, x1=x_center, x2=x_center + target_width)

    audio_clip = concatenate_audioclips([AudioFileClip("./output/title.mp3"), AudioFileClip("./output/temp.mp3")])
    video_export = cropped_clip.set_audio(audio_clip)
    video_export = resize(video_export, width=1080, height=1920)
    # Write the final video with text to a file
    video_export.write_videofile(f"./output/{file_name}.mp4", codec="mpeg4", fps=video_export.fps, bitrate="30000k")
    crop_vertical(file_name)
    



class QueueProcessor:
    def __init__(self):
        self.video_queue = queue.Queue()
        self.is_processing = False

    def add_to_queue(self, obj):
        self.video_queue.put(obj)

    def process_queue(self):
        while not self.video_queue.empty():
            video = self.video_queue.get()
            processOnePost(video['file'], video['title'], video['ss'], video['text'])
        print("stopped")


def add_to_queue():
    file_text = file.get()
    title_text = title.get()
    ss_text = screenshot.get()
    text_text = text.get("1.0", tk.END).strip()
    print(text_text)

    if file_text and title_text and ss_text and text_text:
        processor.add_to_queue({"file": file_text, "title": title_text, "ss": ss_text, "text": text_text})
        file.delete(0, tk.END)
        title.delete(0, tk.END)
        screenshot.delete(0, tk.END)
        text.delete("1.0", tk.END)

def start_processing():
    if not processor.is_processing:
        processor.is_processing = True
        processing_thread = threading.Thread(target=processor.process_queue)
        processing_thread.daemon = True
        processing_thread.start()
        start_button.config(state=tk.DISABLED)


processor = QueueProcessor()

root = tk.Tk()
root.title("Queue Videos")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

file_label = tk.Label(frame, text="Enter File")
file_label.pack()

file = tk.Entry(frame)
file.pack()


title_label = tk.Label(frame, text="Enter Title")
title_label.pack()

title = tk.Entry(frame)
title.pack()


screenshot_label = tk.Label(frame, text="Enter Screenshot")
screenshot_label.pack()

screenshot = tk.Entry(frame)
screenshot.pack()

text_label = tk.Label(frame, text="Enter Text")
text_label.pack()

text = tk.Text(frame, wrap=tk.WORD, height=10, width=40)
text.pack()

add_button = tk.Button(frame, text="Add to Queue", command=add_to_queue)
add_button.pack()

start_button = tk.Button(frame, text="Start Processing", command=start_processing)
start_button.pack()

root.mainloop()





# input_file_name = input("Enter Saved Name:\n")
# input_title = input("Enter Title:\n")
# screenshot = "./input/screenshot.png"
# input_string = input("Enter text:\n")

# processOnePost(input_file_name, input_title, input_string, screenshot)




