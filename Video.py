from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip,VideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def merge_videos(video_clip1, video_clip2, audio=True):
    # Об'єднуємо два відеокліпи
    if audio:
        final_clip = concatenate_videoclips([video_clip1, video_clip2])
    else:
        # Встановлюємо None для аудіо у вихідному відеокліпі
        video_clip1_noaudio = video_clip1.set_audio(None)
        video_clip2_noaudio = video_clip2.set_audio(None)
        final_clip = concatenate_videoclips([video_clip1_noaudio, video_clip2_noaudio])
    # Звільняємо ресурси, пов'язані з відеокліпами, після використання
    del video_clip1
    del video_clip2

    return final_clip


def trim_video(video_clip, time):
    # Виріжте відео за допомогою subclip
    trimmed_clip = video_clip.subclip(0, time)
    return trimmed_clip

def overlay_audio(video_clip, audio_clip):

    return video_clip.set_audio(audio_clip)