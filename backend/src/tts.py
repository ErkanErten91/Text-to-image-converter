import os
from gtts import gTTS

class TextToSpeech:
    def __init__(self):
        pass

    def generate_speech(self, text: str, language: str = 'de', voice: str = 'anna', 
                       speech_speed: str = 'normal', is_preview: bool = False) -> str:
        """
        Converts text to speech and saves it to an audio file.
        """
        try:
            print(f"🔊 Generating speech: {language}, voice: {voice}, speed: {speech_speed}")
            
            # Erstelle Ausgabepfad
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generiere eindeutigen Dateinamen
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            prefix = "preview_" if is_preview else "full_"
            output_file = os.path.join(output_dir, f"{prefix}{text_hash}.mp3")
            
            # Verwende gTTS für Text-zu-Sprache
            tts = gTTS(text=text, lang=language, slow=(speech_speed == 'slow'))
            tts.save(output_file)
            
            print(f"✅ Speech generated: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error generating speech: {str(e)}")
            return None

    def preview_translation(self, text: str, target_language: str) -> dict:
        """
        Zeigt Vorschau der Übersetzung
        """
        try:
            # Einfache Übersetzungsvorschau
            translations = {
                'de': 'Deutscher Text',
                'en': 'English text',
                'es': 'Texto en español',
                'fr': 'Texte français'
            }
            
            return {
                'original_text': text,
                'target_language': target_language,
                'estimated_translation': translations.get(target_language, text),
                'estimated_duration': len(text.split()) * 0.5  # Sekunden
            }
            
        except Exception as e:
            return {'error': str(e)}
