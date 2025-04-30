import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

# Step 1: Configuration
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set!")

# Step 2: Audio Playback Function (Universal)
def play_audio(output_filepath):
    """Play audio file automatically based on the operating system."""
    if not os.path.exists(output_filepath):
        raise FileNotFoundError(f"Audio file not found: {output_filepath}")
    
    os_name = platform.system()
    print(f"Detected OS: {os_name}")  # Debug output
    
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            # Try two different methods for Windows
            try:
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync()'])
            except:
                subprocess.run(['start', output_filepath], shell=True)
        elif os_name == "Linux":
            # Try multiple Linux audio players
            try:
                subprocess.run(['aplay', output_filepath])
            except FileNotFoundError:
                try:
                    subprocess.run(['mpg123', output_filepath])
                except FileNotFoundError:
                    subprocess.run(['ffplay', '-autoexit', output_filepath])
        else:
            print(f"Unsupported OS: {os_name}. Audio saved at: {output_filepath}")
    except Exception as e:
        print(f"Error playing audio: {e}")

# Step 3: Text-to-Speech with gTTS (Google)
def text_to_speech_with_gtts(input_text, output_filepath="gtts_output.mp3"):
    """Convert text to speech using Google's gTTS with auto-playback."""
    try:
        audio = gTTS(text=input_text, lang="en", slow=False)
        audio.save(output_filepath)
        print(f"Audio saved to: {output_filepath}")
        play_audio(output_filepath)
    except Exception as e:
        print(f"Error in gTTS conversion: {e}")

# Step 4: Text-to-Speech with ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_output.mp3"):
    """Convert text to speech using ElevenLabs with auto-playback."""
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="River",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        print(f"Audio saved to: {output_filepath}")
        play_audio(output_filepath)
    except Exception as e:
        print(f"Error in ElevenLabs conversion: {e}")

# Step 5: Main Execution
if __name__ == "__main__":
    test_text = "Hello, this is hi ucchansh"
    
    # Uncomment which service you want to test
    text_to_speech_with_gtts(test_text, "gtts_test.mp3")
    # text_to_speech_with_elevenlabs(test_text, "elevenlabs_test.mp3")