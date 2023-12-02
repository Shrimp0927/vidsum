from openai import OpenAI
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from moviepy.editor import *

file_name = input("Enter your video file name>>\n")
output_audio_file_name = input("Enter the desired name for the output audio file")



# Make sure you are passing the path to your video as the first argument
audio = VideoFileClip(file_name + ".mp4").audio
audio.write_audiofile(output_audio_file_name + ".mp3", codec="mp3")

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

audio_file = open(output_audio_file_name + ".mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You will summarize any inputs"},
    {"role": "user", "content": transcript},
  ]
)

print(response['choices'][0]['message']['content'])
