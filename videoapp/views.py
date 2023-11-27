import tempfile
from django.shortcuts import render
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from django.templatetags.static import static
import os
from io import BytesIO
from django.conf import settings
import base64
from moviepy.config import change_settings


change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick\\magick.exe"}) 

def index(request):
    return render(request, 'videoapp/index.html')

def generate_video(username, video_template_path, text_position, text_duration,fontsize, font, color, bg_color,):
    video = VideoFileClip(video_template_path)

    # Create a TextClip with the animated typing effect for the username
    txt_clip = TextClip(username,fontsize=fontsize, font=font, color=color, bg_color=bg_color).set_duration(video.duration)

    # Set the position of the text and duration
    txt_clip = txt_clip.set_position(text_position).set_duration(text_duration[0] - text_duration[1]).set_start(text_duration[1])

    # Overlay the TextClip on the video
    final_video = CompositeVideoClip([video, txt_clip])

    # Create a temporary file to store the video
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_filename = temp_file.name
        print(f"Temp Filename: {temp_filename}")
        final_video.write_videofile(temp_filename, codec='libx264', audio_codec='aac', remove_temp=True)

    with open(temp_filename, 'rb') as video_file:
        video_data = video_file.read()

    # Encode the binary data in base64
    video_data_base64 = base64.b64encode(video_data).decode('utf-8')

    return video_data_base64

def display_demo(request):
    video_list = [
        {'id': 1, 'name': 'Video 1', 'template_path': 'videoapp/demo/demo.mp4'},
        {'id': 2, 'name': 'Video 2', 'template_path': 'videoapp/demo/demo2.mp4'},
        # Add more videos as needed
    ]

    return render(request, 'videoapp/demo.html', {'video_list': video_list})

def user_input(request):
    video_list = [
        {'id': 1, 'name': 'Video 1', 'template_path': 'videoapp/demo/demo_template.mp4', 'text_position': (230, 483), 'text_duration': (4.55, 0.7),'fontsize':45, 'font':'Arial', 'color':'black', 'bg_color':'#F2F2F2'},
        {'id': 2, 'name': 'Video 2', 'template_path': 'videoapp/demo/demo2.mp4', 'text_position': (434, 495), 'text_duration': (4.9, 0.4), 'fontsize':120,'font':'Arial', 'color':'black', 'bg_color':'#F2F2F2'},
        # Add more videos as needed
    ]

    if request.method == 'POST':
        username = request.POST.get('username', '')
        video_id = int(request.POST.get('video_id', '1'))  # Default to Video 1 if not selected

        selected_video = next((video for video in video_list if video['id'] == video_id), None)

        if selected_video:
            video_template_path = os.path.join(settings.STATIC_ROOT, selected_video['template_path'])
            text_position = selected_video['text_position']
            text_duration = selected_video['text_duration']
            fontsize = selected_video['fontsize']
            font = selected_video['font']
            color = selected_video['color']
            bg_color = selected_video['bg_color']

            video_data_base64 = generate_video(username, video_template_path, text_position, text_duration,fontsize, font, color, bg_color)

            return render(request, 'videoapp/generated_video.html', {'username': username, 'video_data': video_data_base64, 'video_type': 'video/mp4'})

    return render(request, 'videoapp/user_input.html', {'video_list': video_list})
