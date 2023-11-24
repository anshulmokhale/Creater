from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load the video
video = VideoFileClip("newVide.mp4")

# Get the duration of the video in seconds
video_duration = video.duration

# Create a text clip with desired text
text_clip = TextClip('Ansul Mokhale', fontsize=70, color='black')
# You can adjust the text properties as needed

# Position the text clip at a specific time (e.g., halfway through the video)
text_start_time = video_duration / 2
text_clip = text_clip.set_position(('center', 'bottom')).set_start(text_start_time)

# Overlay text onto the video
final_video = CompositeVideoClip([video.set_duration(video_duration), text_clip.set_duration(video_duration)])

# Export the video with text overlay
final_video.write_videofile("output_video.mp4", codec='libx264', fps=video.fps)
