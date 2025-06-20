'''
import os
import yt_dlp as youtube_dl

# Set video URL and output directory
video_url = 'https://youtu.be/Ujuwxc4pfgo?si=TOU9qVKCyKp8yjSS'
output_dir = 'D:/path/to/save/'  # Ensure this path is valid on your system

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define yt-dlp options
ydl_opts = {
    'format': 'best',  # Best video up to 1080p and best audio
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Save video with title as filename
}

try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading video from {video_url}...")
        ydl.download([video_url])
        print('Video downloaded successfully!')
except youtube_dl.utils.DownloadError as e:
    print(f"DownloadError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
'''

'''

import os
import yt_dlp as youtube_dl

video_url = 'https://youtu.be/Ujuwxc4pfgo?si=fBWEiC_AeaLHp9Ng'  # Replace with your actual video URL
output_dir = 'D:/path/to/save/'  # Replace with your desired directory path

# Ensure the output directory exists, create it if it doesn't
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Replace 'format_code' with the actual format code you want
video_format = '137'  # Example: '137' for 1080p video
audio_format = '140'  # Example: '140' for best audio

# Define options for yt-dlp to download video
ydl_opts_video = {
    'format': video_format,
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
}

# Define options for yt-dlp to download audio
ydl_opts_audio = {
    'format': audio_format,
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
}

try:
    with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
        ydl.download([video_url])
    
    with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([video_url])
    
    print('Video and audio downloaded successfully!')
except Exception as e:
    print(f"An error occurred: {e}")


'''


'''

from moviepy.editor import VideoFileClip, AudioFileClip

# Paths to your video and audio files
video_path = 'D:/path/to/save/video.mp4'
audio_path = 'D:/path/to/save/audio.mp3'
output_path = 'D:/path/to/save/output_video.mp4'

# Load the video and audio
video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(audio_path)

# Set the audio of the video to the audio file
final_clip = video_clip.set_audio(audio_clip)

# Write the result to a file
final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
'''
'''
import subprocess

video_file = "D:/path/to/save/video.mp4"
audio_file = "D:/path/to/save/audio.mp3"
output_file = "D:/path/to/save/output.mp4"

# Attempt to use copy command (not suited for media merging)
subprocess.run(f'copy /b "{video_file}" + "{audio_file}" "{output_file}"', shell=True)

print(f"Merged video and audio saved as {output_file}")

'''