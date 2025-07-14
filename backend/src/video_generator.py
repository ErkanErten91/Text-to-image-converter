import os
import moviepy.editor as mp
from moviepy.config import change_settings

# Setze den Pfad zu FFmpeg
ffmpeg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ffmpeg', 'ffmpeg.exe')
if os.path.exists(ffmpeg_path):
    change_settings({"FFMPEG_BINARY": ffmpeg_path})
    print(f"Found FFmpeg at: {ffmpeg_path}")

class VideoGenerator:
    def __init__(self):
        pass

    def create_video(self, audio_file: str, text: str, resolution: str = '1080p', 
                    style: str = 'explainer', music: str = 'none', is_preview: bool = False):
        """
        Creates a video using the provided audio file and text.
        """
        try:
            # Überprüfe, ob die Audiodatei existiert
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
            print(f"🎬 Creating video: {resolution}, style: {style}")
            
            # Erstelle Ausgabepfad
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            prefix = "preview_" if is_preview else "video_"
            output_file = os.path.join(output_dir, f"{prefix}{os.path.basename(audio_file).split('.')[0]}.mp4")
            
            # Lade die Audiodatei
            audio_clip = mp.AudioFileClip(audio_file)
            
            # Bestimme Auflösung
            if resolution == '720p':
                size = (1280, 720)
            elif resolution == '1440p':
                size = (2560, 1440)
            elif resolution == '2160p':
                size = (3840, 2160)
            else:  # 1080p default
                size = (1920, 1080)
            
            # Erstelle Text-Clip basierend auf Stil
            if style == 'minimal':
                txt_clip = mp.TextClip(text, fontsize=40, color='white', bg_color='black', size=size)
            elif style == 'presentation':
                txt_clip = mp.TextClip(text, fontsize=50, color='white', bg_color='navy', size=size)
            elif style == 'tutorial':
                txt_clip = mp.TextClip(text, fontsize=45, color='yellow', bg_color='darkblue', size=size)
            else:  # explainer default
                txt_clip = mp.TextClip(text, fontsize=35, color='white', bg_color='darkgreen', size=size)
            
            txt_clip = txt_clip.set_duration(audio_clip.duration)
            
            # Kombiniere Audio und Text
            video_clip = txt_clip.set_audio(audio_clip)
            
            # Schreibe das Video
            fps = 24 if is_preview else 30
            bitrate = '2000k' if is_preview else '5000k'
            
            video_clip.write_videofile(
                output_file, 
                fps=fps, 
                codec='libx264',
                bitrate=bitrate,
                verbose=False,
                logger=None
            )
            
            # Cleanup
            audio_clip.close()
            txt_clip.close()
            video_clip.close()
            
            print(f"✅ Video created: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error creating video: {str(e)}")
            return None
