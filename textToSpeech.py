import requests
from isFemale import is_female

def generate_tts(text):
    # Constants
    CHUNK_SIZE = 1024
    XI_API_KEY = "a1c36e67bb5fd426c2452069e02afe4e"
    OUTPUT_PATH = "assets/audio.mp3"

    voice_id = "pNInz6obpgDQGcFmaJgB"
    #if(is_female(text) == 'f'):
     #   voice_id = "jsCqWAovK2LkecY7zXl4"

    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    # Headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Data payload for the API request, including the text and voice settings
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        print("Audio stream saved successfully to", OUTPUT_PATH)
    else:
        print("Failed to generate TTS:", response.text)

# Example usage
text_example = "I (29F) was getting married to my now-husband (32M), and my MIL(59) was invited to the wedding, of course..."

generate_tts(text_example)

