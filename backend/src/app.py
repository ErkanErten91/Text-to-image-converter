from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS
from tts import TextToSpeech
from video_generator import VideoGenerator
from free_ai_video_generator import FreeAIVideoGenerator
import os
import time
import hashlib
from typing import Optional

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:3000"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

def combine_video_with_audio(video_file, audio_file):
    """Kombiniert AI-Video mit Audio"""
    try:
        print("🎵 Combining AI video with audio...")
        
        if not os.path.exists(video_file) or not os.path.exists(audio_file):
            print("❌ Video or audio file not found")
            return None
        
        import moviepy.editor as mp
        
        # Lade Video und Audio
        video_clip = mp.VideoFileClip(video_file)
        audio_clip = mp.AudioFileClip(audio_file)
        
        print(f"📹 Video duration: {video_clip.duration:.1f}s")
        print(f"🔊 Audio duration: {audio_clip.duration:.1f}s")
        
        # Passe Video-Länge an Audio an
        if video_clip.duration < audio_clip.duration:
            # Video ist kürzer - wiederhole es
            loops_needed = int(audio_clip.duration / video_clip.duration) + 1
            print(f"🔄 Looping video {loops_needed} times to match audio length")
            video_clip = mp.concatenate_videoclips([video_clip] * loops_needed)
        
        # Schneide Video auf Audio-Länge
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
        # Kombiniere Video und Audio
        final_clip = video_clip.set_audio(audio_clip)
        
        # Speichere finales Video
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        final_filename = f"free_ai_final_{int(time.time())}.mp4"
        final_path = os.path.join(output_dir, final_filename)
        
        print("💾 Saving final video...")
        final_clip.write_videofile(
            final_path,
            fps=24,
            codec='libx264',
            bitrate='5000k',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # Cleanup
        video_clip.close()
        audio_clip.close()
        final_clip.close()
        
        print(f"✅ Final FREE AI video created: {final_path}")
        return final_path
        
    except Exception as e:
        print(f"❌ Video-Audio combination failed: {e}")
        return video_file  # Gib wenigstens das Video zurück

@app.route('/api/generate-free-ai-video', methods=['POST'])
def generate_free_ai_video():
    """
    🆓 Generiert Videos mit 100% kostenlosen AI Services
    """
    try:
        data = request.json
        audio_text = data.get('audioText', '') or data.get('text', '')
        video_description = data.get('videoDescription', '')
        
        if not audio_text:
            return jsonify({'error': 'Audio text is required'}), 400
        
        print(f"\n🆓 === FREE AI VIDEO GENERATION ===")
        print(f"📝 Audio Text: {audio_text[:100]}...")
        print(f"🎨 Video Description: {video_description[:100]}...")
        
        # 1. Generiere Audio
        print("🔊 Generating audio...")
        tts = TextToSpeech()
        audio_file = tts.generate_speech(audio_text)
        
        if not audio_file:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
        print(f"✅ Audio generated: {audio_file}")
        
        # 2. Generiere kostenloses AI Video
        print("🤖 Starting FREE AI video generation...")
        generator = FreeAIVideoGenerator()
        
        # Verwende video_description falls vorhanden, sonst audio_text
        video_prompt = video_description if video_description.strip() else audio_text
        
        video_file = generator.generate_professional_video(video_prompt)
        
        if not video_file:
            return jsonify({'error': 'All free AI video services failed'}), 500
        
        print(f"✅ FREE AI Video generated: {video_file}")
        
        # 3. Kombiniere Video mit Audio
        final_video = combine_video_with_audio(video_file, audio_file)
        
        if not final_video:
            # Falls Kombination fehlschlägt, verwende nur das Video
            final_video = video_file
        
        # Erstelle URLs für Frontend
        video_url = f"/output/{os.path.basename(final_video)}"
        audio_url = f"/output/{os.path.basename(audio_file)}"
        
        return jsonify({
            'success': True,
            'url': video_url,
            'audio_url': audio_url,
            'original_text': audio_text,
            'video_description': video_description,
            'processing_time': time.time(),
            'is_ai_generated': True,
            'service_used': 'free_ai_services',
            'cost': 'FREE'
        }), 200
        
    except Exception as e:
        print(f"❌ Error in FREE AI video generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'FREE AI video generation failed: {str(e)}'}), 500

@app.route('/api/generate-ai-video', methods=['POST'])
def generate_ai_video():
    """
    🎬 Hauptendpunkt für AI-Video-Generierung (nur FREE Services)
    """
    try:
        data = request.json
        audio_text = data.get('audioText', '') or data.get('text', '')
        video_description = data.get('videoDescription', '')
        options = data.get('options', {})
        
        if not audio_text:
            return jsonify({'error': 'Audio text is required'}), 400
        
        print(f"\n🎬 === AI VIDEO GENERATION ===")
        print(f"📝 Audio Text: {audio_text[:100]}...")
        print(f"🎨 Video Description: {video_description[:100]}...")
        print(f"⚙️ Options: {options}")
        
        # 1. Generiere Audio
        print("🔊 Generating audio...")
        tts = TextToSpeech()
        audio_file = tts.generate_speech(audio_text)
        
        if not audio_file:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
        print(f"✅ Audio generated: {audio_file}")
        
        # 2. Verwende FREE AI Services
        print("🆓 Using FREE AI Services...")
        generator = FreeAIVideoGenerator()
        video_prompt = video_description if video_description.strip() else audio_text
        video_file = generator.generate_professional_video(video_prompt)
        service_used = 'free_ai_services'
        
        if not video_file:
            return jsonify({'error': 'All AI video services failed'}), 500
        
        print(f"✅ AI Video generated: {video_file}")
        
        # 3. Kombiniere mit Audio
        final_video = combine_video_with_audio(video_file, audio_file)
        if not final_video:
            final_video = video_file
        
        # Erstelle URLs für Frontend
        video_url = f"/output/{os.path.basename(final_video)}"
        audio_url = f"/output/{os.path.basename(audio_file)}"
        
        return jsonify({
            'success': True,
            'url': video_url,
            'audio_url': audio_url,
            'original_text': audio_text,
            'video_description': video_description,
            'options': options,
            'processing_time': time.time(),
            'is_ai_generated': True,
            'service_used': service_used,
            'cost': 'FREE'
        }), 200
        
    except Exception as e:
        print(f"❌ Error in AI video generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'AI video generation failed: {str(e)}'}), 500

@app.route('/api/test-free-services', methods=['GET'])
def test_free_services():
    """
    🧪 Teste alle kostenlosen AI Services
    """
    try:
        generator = FreeAIVideoGenerator()
        
        # Teste alle Services
        results = generator.test_all_services()
        
        # Service Status
        service_status = generator.get_service_status()
        
        # Working Spaces
        working_spaces = generator.get_working_spaces_list()
        
        return jsonify({
            'test_results': results,
            'service_status': service_status,
            'working_spaces': working_spaces,
            'generator_status': generator.get_status()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/free-ai-status', methods=['GET'])
def get_free_ai_status():
    """
    📊 Status der kostenlosen AI Services
    """
    try:
        generator = FreeAIVideoGenerator()
        
        return jsonify({
            'status': 'available',
            'services': generator.get_service_status(),
            'working_spaces': generator.get_working_spaces_list(),
            'generator_info': generator.get_status(),
            'cost': 'FREE',
            'billing_required': False
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    tts = TextToSpeech()
    audio_file = tts.generate_speech(text)
    
    if not audio_file:
        return jsonify({'error': 'Failed to generate speech'}), 500
    
    return jsonify({'audio_file': audio_file}), 200

@app.route('/api/video', methods=['POST'])
def generate_video():
    data = request.json
    text = data.get('text')
    audio_file = data.get('audio_file')
    
    if not text:
        return jsonify({'error': 'Text must be provided'}), 400
    
    if not audio_file:
        tts = TextToSpeech()
        audio_file = tts.generate_speech(text)
        
        if not audio_file:
            return jsonify({'error': 'Failed to generate speech'}), 500
    
    video_generator = VideoGenerator()
    video_file = video_generator.create_video(audio_file, text)
    
    if not video_file:
        return jsonify({'error': 'Failed to generate video'}), 500
    
    return jsonify({'video_file': video_file}), 200

@app.route('/api/generate-video', methods=['POST'])
def generate_video_direct():
    """
    Kombinierter Endpunkt für Standard-Video-Generierung
    """
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Text zu Sprache
    tts = TextToSpeech()
    audio_file = tts.generate_speech(text)
    
    if not audio_file:
        return jsonify({'error': 'Failed to generate speech'}), 500
    
    # Sprache zu Video
    video_generator = VideoGenerator()
    video_file = video_generator.create_video(audio_file, text)
    
    if not video_file:
        return jsonify({'error': 'Failed to generate video'}), 500
    
    video_url = f"/output/{os.path.basename(video_file)}"
    
    return jsonify({'url': video_url}), 200

@app.route('/output/<filename>')
def serve_file(filename):
    """
    Dient dazu, generierte Dateien an das Frontend zu senden.
    """
    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path)
        
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({'error': f'Failed to serve file: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health-Check Endpunkt
    """
    try:
        return jsonify({
            'status': 'healthy',
            'message': 'FREE AI Text-to-Video API is running',
            'timestamp': time.time(),
            'services': {
                'tts': 'available',
                'video_generator': 'available',
                'free_ai_services': 'available'
            },
            'version': '3.0.0'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup_files():
    """
    Löscht alte generierte Dateien
    """
    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        
        if not os.path.exists(output_dir):
            return jsonify({'message': 'No files to cleanup'}), 200
        
        deleted_files = 0
        total_size = 0
        
        for filename in os.listdir(output_dir):
            if filename.endswith(('.mp3', '.mp4', '.wav', '.avi')):
                file_path = os.path.join(output_dir, filename)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_files += 1
                    total_size += file_size
                except Exception as e:
                    print(f"Error deleting {filename}: {str(e)}")
                            # Konvertiere Bytes zu MB
        total_size_mb = total_size / (1024 * 1024)
        
        return jsonify({
            'message': f'Cleanup completed. {deleted_files} files deleted.',
            'deleted_files': deleted_files,
            'freed_space_mb': round(total_size_mb, 2)
        }), 200
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def get_system_status():
    """
    Gibt detaillierte Systeminformationen zurück.
    """
    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        
        # Zähle Dateien im Output-Verzeichnis
        file_count = 0
        total_size = 0
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                if filename.endswith(('.mp3', '.mp4', '.wav', '.avi')):
                    file_path = os.path.join(output_dir, filename)
                    file_count += 1
                    total_size += os.path.getsize(file_path)
        
        return jsonify({
            'system': {
                'status': 'running',
                'uptime': time.time(),
                'version': '3.0.0'
            },
            'storage': {
                'output_files': file_count,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'output_directory': output_dir
            },
            'services': {
                'tts': 'available',
                'video_generator': 'available',
                'free_ai_services': 'available'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tts/validate', methods=['POST'])
def validate_text():
    """
    Validiert den eingegebenen Text
    """
    data = request.json
    text = data.get('text', '')
    
    errors = []
    warnings = []
    
    # Basis-Validierung
    if not text or not text.strip():
        errors.append('Text darf nicht leer sein')
    
    if len(text) > 5000:
        errors.append('Text ist zu lang (max. 5000 Zeichen)')
    
    if len(text) < 10:
        errors.append('Text ist zu kurz (min. 10 Zeichen)')
    
    # Warnungen hinzufügen
    word_count = len(text.split())
    if word_count > 500:
        warnings.append('Sehr langer Text - Videogenerierung kann länger dauern')
    
    if len(text) > 2000:
        warnings.append('Langer Text - erwäge eine Aufteilung in mehrere Videos')
    
    # Prüfe auf spezielle Zeichen
    if any(char in text for char in ['@', '#', '```', '%']):
        warnings.append('Spezielle Zeichen können die Sprachqualität beeinträchtigen')
    
    return jsonify({
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'wordCount': word_count,
        'charCount': len(text)
    })

@app.route('/api/tts/optimal-settings', methods=['POST'])
def get_optimal_settings():
    """
    Gibt optimale TTS-Einstellungen basierend auf dem Text zurück
    """
    data = request.json
    text = data.get('text', '')
    
    # Einfache Logik für optimale Einstellungen
    word_count = len(text.split())
    
    if word_count < 50:
        speed = 'normal'
        voice = 'anna'
        resolution = '720p'
        style = 'explainer'
    elif word_count < 200:
        speed = 'normal'
        voice = 'max'
        resolution = '1080p'
        style = 'presentation'
    else:
        speed = 'slow'
        voice = 'anna'
        resolution = '1080p'
        style = 'tutorial'
    
    return jsonify({
        'recommended_settings': {
            'language': 'de',
            'voice': voice,
            'speechSpeed': speed,
            'resolution': resolution,
            'style': style,
            'music': 'none'
        },
        'analysis': {
            'word_count': word_count,
            'char_count': len(text),
            'estimated_duration': f"{word_count * 0.5:.1f} Sekunden",
            'complexity': 'einfach' if word_count < 100 else 'mittel' if word_count < 300 else 'komplex'
        },
        'suggestions': [
            f"Text hat {word_count} Wörter",
            f"Empfohlene Stimme: {voice}",
            f"Empfohlene Geschwindigkeit: {speed}"
        ]
    })

@app.route('/api/tts/languages', methods=['GET'])
def get_languages():
    """
    Gibt verfügbare Sprachen zurück
    """
    languages = [
        {'code': 'de', 'name': 'Deutsch'},
        {'code': 'en', 'name': 'English'},
        {'code': 'es', 'name': 'Español'},
        {'code': 'fr', 'name': 'Français'},
        {'code': 'it', 'name': 'Italiano'}
    ]
    return jsonify(languages)

@app.route('/api/tts/voices', methods=['GET'])
def get_voices():
    """
    Gibt verfügbare Stimmen zurück
    """
    voices = [
        {'code': 'anna', 'name': 'Anna (Weiblich)', 'gender': 'female'},
        {'code': 'max', 'name': 'Max (Männlich)', 'gender': 'male'},
        {'code': 'clara', 'name': 'Clara (Weiblich)', 'gender': 'female'},
        {'code': 'david', 'name': 'David (Männlich)', 'gender': 'male'}
    ]
    return jsonify(voices)

@app.route('/api/tts/speeds', methods=['GET'])
def get_speech_speeds():
    """
    Gibt verfügbare Sprechgeschwindigkeiten zurück
    """
    speeds = [
        {'code': 'slow', 'name': 'Langsam', 'value': 0.8},
        {'code': 'normal', 'name': 'Normal', 'value': 1.0},
        {'code': 'fast', 'name': 'Schnell', 'value': 1.2}
    ]
    return jsonify(speeds)

@app.route('/api/video/resolutions', methods=['GET'])
def get_resolutions():
    """
    Gibt verfügbare Video-Auflösungen zurück
    """
    resolutions = [
        {'code': '720p', 'name': '720p (HD)', 'width': 1280, 'height': 720},
        {'code': '1080p', 'name': '1080p (Full HD)', 'width': 1920, 'height': 1080},
        {'code': '1440p', 'name': '1440p (2K)', 'width': 2560, 'height': 1440},
        {'code': '2160p', 'name': '2160p (4K)', 'width': 3840, 'height': 2160}
    ]
    return jsonify(resolutions)

@app.route('/api/video/styles', methods=['GET'])
def get_video_styles():
    """
    Gibt verfügbare Video-Stile zurück
    """
    styles = [
        {'code': 'explainer', 'name': 'Erklärvideo', 'description': 'Einfach und klar'},
        {'code': 'presentation', 'name': 'Präsentation', 'description': 'Professionell'},
        {'code': 'tutorial', 'name': 'Tutorial', 'description': 'Schritt-für-Schritt'},
        {'code': 'storytelling', 'name': 'Storytelling', 'description': 'Erzählend'},
        {'code': 'news', 'name': 'Nachrichten', 'description': 'Sachlich'},
        {'code': 'minimal', 'name': 'Minimal', 'description': 'Schlicht'}
    ]
    return jsonify(styles)

@app.route('/api/video/music', methods=['GET'])
def get_music_options():
    """
    Gibt verfügbare Hintergrundmusik-Optionen zurück
    """
    music = [
        {'code': 'none', 'name': 'Keine Musik'},
        {'code': 'ambient', 'name': 'Ambient', 'description': 'Ruhig und atmosphärisch'},
        {'code': 'corporate', 'name': 'Corporate', 'description': 'Professionell'},
        {'code': 'upbeat', 'name': 'Upbeat', 'description': 'Energisch'},
        {'code': 'calm', 'name': 'Calm', 'description': 'Entspannend'},
        {'code': 'dramatic', 'name': 'Dramatic', 'description': 'Spannend'}
    ]
    return jsonify(music)

@app.route('/api/options', methods=['GET'])
def get_available_options():
    """
    Gibt alle verfügbaren Optionen zurück
    """
    try:
        options = {
            'languages': [
                {'code': 'de', 'name': 'Deutsch'},
                {'code': 'en', 'name': 'English'},
                {'code': 'es', 'name': 'Español'},
                {'code': 'fr', 'name': 'Français'},
                {'code': 'it', 'name': 'Italiano'}
            ],
            'voices': [
                {'code': 'anna', 'name': 'Anna (Weiblich)'},
                {'code': 'max', 'name': 'Max (Männlich)'},
                {'code': 'clara', 'name': 'Clara (Weiblich)'},
                {'code': 'david', 'name': 'David (Männlich)'}
            ],
            'speechSpeeds': [
                {'code': 'slow', 'name': 'Langsam'},
                {'code': 'normal', 'name': 'Normal'},
                {'code': 'fast', 'name': 'Schnell'}
            ],
            'resolutions': [
                {'code': '720p', 'name': '720p (HD)'},
                {'code': '1080p', 'name': '1080p (Full HD)'},
                {'code': '1440p', 'name': '1440p (2K)'},
                {'code': '2160p', 'name': '2160p (4K)'}
            ],
            'styles': [
                {'code': 'explainer', 'name': 'Erklärvideo'},
                {'code': 'presentation', 'name': 'Präsentation'},
                {'code': 'tutorial', 'name': 'Tutorial'},
                {'code': 'storytelling', 'name': 'Storytelling'},
                {'code': 'news', 'name': 'Nachrichten'},
                {'code': 'minimal', 'name': 'Minimal'}
            ],
            'music': [
                {'code': 'none', 'name': 'Keine Musik'},
                {'code': 'ambient', 'name': 'Ambient'},
                {'code': 'corporate', 'name': 'Corporate'},
                {'code': 'upbeat', 'name': 'Upbeat'},              
                {'code': 'calm', 'name': 'Calm'},
                {'code': 'dramatic', 'name': 'Dramatic'}
            ],
            'ai_features': {
                'available': True,
                'free_services': True,
                'models': [
                    {'code': 'huggingface', 'name': 'Hugging Face Spaces'},
                    {'code': 'free-ai', 'name': 'Free AI Services'}
                ]
            }
        }
        
        return jsonify(options), 200
        
    except Exception as e:
        print(f"Error getting options: {str(e)}")
        return jsonify({'error': f'Failed to get options: {str(e)}'}), 500

@app.route('/api/video-templates', methods=['GET'])
def get_video_templates():
    """
    Gibt vordefinierte Video-Templates zurück
    """
    templates = [
        {
            'id': 'explainer',
            'name': 'Erklärvideo',
            'description': 'Perfekt für Tutorials und Erklärungen',
            'settings': {
                'style': 'explainer',
                'resolution': '1080p',
                'music': 'ambient',
                'voice': 'anna',
                'speechSpeed': 'normal'
            }
        },
        {
            'id': 'presentation',
            'name': 'Präsentation',
            'description': 'Professionell für Business-Inhalte',
            'settings': {
                'style': 'presentation',
                'resolution': '1080p',
                'music': 'corporate',
                'voice': 'max',
                'speechSpeed': 'normal'
            }
        },
        {
            'id': 'storytelling',
            'name': 'Storytelling',
            'description': 'Für Geschichten und Narrative',
            'settings': {
                'style': 'storytelling',
                'resolution': '1080p',
                'music': 'dramatic',
                'voice': 'clara',
                'speechSpeed': 'slow'
            }
        },
        {
            'id': 'free_ai',
            'name': 'FREE AI Video',
            'description': '100% kostenlose KI-generierte Videos',
            'settings': {
                'style': 'ai_generated',
                'resolution': '1080p',
                'music': 'none',
                'voice': 'anna',
                'speechSpeed': 'normal',
                'ai_enhanced': True
            }
        }
    ]
    
    return jsonify(templates)

@app.route('/api/apply-template', methods=['POST'])
def apply_template():
    """
    Wendet ein Video-Template an
    """
    try:
        data = request.json
        text = data.get('text')
        template_id = data.get('template_id')
        
        if not text or not template_id:
            return jsonify({'error': 'Text and template_id required'}), 400
        
        # Lade Template
        templates_response = get_video_templates()
        templates = templates_response.get_json()
        
        template = next((t for t in templates if t['id'] == template_id), None)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        print(f"🎨 Applying template '{template['name']}' to text: {text[:50]}...")
        
        # Verwende Template-Einstellungen
        settings = template['settings']
        
        # Generiere Audio
        tts = TextToSpeech()
        audio_file = tts.generate_speech(text)
        
        if not audio_file:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
        # Generiere Video basierend auf Template
        if settings.get('ai_enhanced', False):
            # Verwende FREE AI Generator
            generator = FreeAIVideoGenerator()
            video_file = generator.generate_professional_video(text)
            
            if video_file:
                # Kombiniere mit Audio
                final_video = combine_video_with_audio(video_file, audio_file)
                video_file = final_video if final_video else video_file
        else:
            # Verwende Standard Generator
            video_generator = VideoGenerator()
            video_file = video_generator.create_video(audio_file, text)
        
        if not video_file:
            return jsonify({'error': 'Failed to generate video'}), 500
        
        # URLs erstellen
        video_url = f"/output/{os.path.basename(video_file)}"
        audio_url = f"/output/{os.path.basename(audio_file)}"
        
        return jsonify({
            'success': True,
            'url': video_url,
            'audio_url': audio_url,
            'template_used': template,
            'settings_applied': settings
        }), 200
        
    except Exception as e:
        print(f"❌ Template application error: {str(e)}")
        return jsonify({'error': f'Template application failed: {str(e)}'}), 500

@app.route('/api/batch-generate', methods=['POST'])
def batch_generate():
    """
    Generiert mehrere Videos auf einmal
    """
    try:
        data = request.json
        texts = data.get('texts', [])
        options = data.get('options', {})
        use_ai = options.get('use_ai', False)
        
        if not texts or len(texts) == 0:
            return jsonify({'error': 'No texts provided'}), 400
        
        if len(texts) > 10:
            return jsonify({'error': 'Maximum 10 texts allowed per batch'}), 400
        
        print(f"🎬 Batch generating {len(texts)} videos (AI: {use_ai})...")
        
        results = []
        
        for i, text in enumerate(texts):
            try:
                print(f"📹 Processing video {i+1}/{len(texts)}: {text[:50]}...")
                
                # Generiere Audio
                tts = TextToSpeech()
                audio_file = tts.generate_speech(text)
                
                if not audio_file:
                    results.append({
                        'index': i,
                        'text': text,
                        'success': False,
                        'error': 'Failed to generate audio'
                    })
                    continue
                
                # Generiere Video
                if use_ai:
                    # Verwende FREE AI Generator
                    generator = FreeAIVideoGenerator()
                    video_file = generator.generate_professional_video(text)
                    
                    if video_file:
                        # Kombiniere mit Audio
                        final_video = combine_video_with_audio(video_file, audio_file)
                        video_file = final_video if final_video else video_file
                else:
                    # Verwende Standard Generator
                    video_generator = VideoGenerator()
                    video_file = video_generator.create_video(audio_file, text)
                
                if not video_file:
                    results.append({
                        'index': i,
                        'text': text,
                        'success': False,
                        'error': 'Failed to generate video'
                    })
                    continue
                
                # Erfolg
                video_url = f"/output/{os.path.basename(video_file)}"
                audio_url = f"/output/{os.path.basename(audio_file)}"
                
                results.append({
                    'index': i,
                    'text': text,
                    'success': True,
                    'video_url': video_url,
                    'audio_url': audio_url,
                    'ai_generated': use_ai
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'text': text,
                    'success': False,
                    'error': str(e)
                })
        
        # Statistiken
        successful = len([r for r in results if r['success']])
        failed = len(results) - successful
        
        return jsonify({
            'batch_results': results,
            'statistics': {
                'total': len(texts),
                'successful': successful,
                'failed': failed,
                'success_rate': round((successful / len(texts)) * 100, 1)
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Batch generation error: {str(e)}")
        return jsonify({'error': f'Batch generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Stelle sicher, dass der Ausgabeordner existiert
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Erstelle auch einen Musik-Ordner für zukünftige Hintergrundmusik
    music_dir = os.path.join(output_dir, 'music')
    os.makedirs(music_dir, exist_ok=True)
    
    print("\n" + "="*70)
    print("🆓 FREE AI TEXT-TO-VIDEO CONVERTER API SERVER v3.0")
    print("="*70)
    print("🚀 Server starting...")
    print(f"📁 Output directory: {output_dir}")
    print(f"🎵 Music directory: {music_dir}")
    print("\n📋 Available endpoints:")
    print("  🆓 POST /api/generate-free-ai-video     - Generate FREE AI video")
    print("  🎬 POST /api/generate-ai-video          - Generate AI video (with fallback)")
    print("  🎬 POST /api/generate-video             - Generate standard video")
    print("  🔊 POST /api/tts                        - Text to speech conversion")
    print("  📹 POST /api/video                      - Generate video from audio")
    print("  🧪 GET  /api/test-free-services         - Test all free services")
    print("  📊 GET  /api/free-ai-status             - Free AI services status")
    print("  ⚙️  GET  /api/options                   - Get available options")
    print("  🎨 GET  /api/video-templates            - Get video templates")
    print("  📝 POST /api/apply-template             - Apply video template")
    print("  📦 POST /api/batch-generate             - Batch generate videos")
    print("  🔍 POST /api/tts/validate               - Validate text input")
    print("  💡 POST /api/tts/optimal-settings       - Get optimal settings")
    print("  🗣️  GET  /api/tts/languages             - Get available languages")
    print("  🎤 GET  /api/tts/voices                 - Get available voices")
    print("  ⚡ GET  /api/tts/speeds                 - Get speech speeds")
    print("  📺 GET  /api/video/resolutions          - Get video resolutions")
    print("  🎭 GET  /api/video/styles               - Get video styles")
    print("  🎵 GET  /api/video/music                - Get music options")
    print("  ❤️  GET  /api/health                    - Health check")
    print("  📊 GET  /api/status                     - System status")
    print("  🧹 POST /api/cleanup                    - Cleanup old files")
    print("  📁 GET  /output/<filename>              - Serve generated files")
    print("="*70)
    print("💰 COST: 100% FREE - NO BILLING REQUIRED")
    print("🤖 AI FEATURES: Hugging Face Spaces + Free Services")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🔧 Debug mode: ON")
    print("="*70 + "\n")
    
    # Teste Free Services beim Start
    try:
        print("🧪 Testing free AI services on startup...")
        
        # Teste ob FreeAIVideoGenerator verfügbar ist
        test_generator = FreeAIVideoGenerator()
        status = test_generator.get_status()
        
        print(f"✅ Free AI Generator Status:")
        print(f"   Services Available: {status.get('services_available', 0)}")
        print(f"   Working Spaces: {len(status.get('working_spaces', []))}")
        print(f"   Generator Ready: {status.get('ready', False)}")
        
        # Teste Hugging Face Token
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        if hf_token:
            print(f"🔑 Hugging Face Token: ✅ (Length: {len(hf_token)})")
        else:
            print("🔑 Hugging Face Token: ⚠️ Not found (some features may be limited)")
        
        # Teste Replicate Token
        replicate_token = os.getenv('REPLICATE_API_TOKEN')
        if replicate_token:
            print(f"🔑 Replicate Token: ✅")
        else:
            print("🔑 Replicate Token: ⚠️ Not found (will use free alternatives)")
        
        print("🎯 Server initialization complete!")
        
    except Exception as e:
        print(f"⚠️ Startup test failed: {e}")
        print("🔄 Server will still start, but some AI features may be limited")
    
    print("\n🚀 Starting Flask server...")
    print("📱 Open your browser and go to: http://localhost:3000")
    print("🔗 API Documentation: http://localhost:5000/api/health")
    print("="*70 + "\n")
    
    # Starte den Server
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
