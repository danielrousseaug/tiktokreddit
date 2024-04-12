import boto3
from isFemale import is_female
import sox

AWS_ACCESS_KEY_ID="AKIARPZ6RCEQD6WCCT6O"
AWS_SECRET_ACCESS_KEY="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"


def generate_tts(text):
    # Constants
    OUTPUT_PATH = "assets/audio.mp3"
    
    # Create a Polly client
    polly = boto3.client('polly', region_name='us-west-2')
    
    # Determine the voice based on the text
    voice_id = "Matthew"
    # if is_female(text) == 'f':
    #     voice_id = "Joanna"
    
    # Make the TTS request to Amazon Polly
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine="neural"
    )
    
    # Check if the request was successful
    if 'AudioStream' in response:
        # Save the audio stream to a file
        with open(OUTPUT_PATH, 'wb') as f:
            f.write(response['AudioStream'].read())
        print("Audio stream saved successfully to", OUTPUT_PATH)
    else:
        print("Failed to generate TTS")
    


def adjust_speed(input_file, output_file, speed):
    # Create a transformer to adjust the speed
    tfm = sox.Transformer()
    tfm.tempo(speed)

    # Apply the speed adjustment to the audio file
    tfm.build(input_file, output_file)
    print("Speed adjustment completed. Output file:", output_file)


# # Example usage
# text_example = "I (29F) was getting married to my now-husband (32M), and my MIL(59) was invited to the wedding, of course..."
# generate_tts(text_example)

# # Adjust the speed of the generated audio file
# input_file = "assets/audio.mp3"
# output_file = "assets/audio_speed_adjusted.mp3"
# speed = 1.5  # Increase the speed by 50%
# adjust_speed(input_file, output_file, speed)