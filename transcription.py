from openai import OpenAI

def format_timestamp(seconds):
    # Format seconds as SRT timestamp (hours:minutes:seconds,milliseconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = round((seconds - int(seconds)) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

def convert_to_srt(transcription, merge_threshold=0.1, max_group_words=3):
    srt_output = ""
    entry_number = 1
    group_start = None
    group_end = None
    grouped_words = []

    def commit_group():
        nonlocal entry_number, srt_output, group_start, group_end, grouped_words
        if grouped_words:
            srt_output += f"{entry_number}\n{format_timestamp(group_start)} --> {format_timestamp(group_end)}\n{' '.join(grouped_words)}\n\n"
            entry_number += 1
            grouped_words = []

    for word_data in transcription:
        start_time = word_data['start']
        end_time = word_data['end']
        word = word_data['word']

        if group_start is None:
            # Start a new group with the current word
            group_start = start_time
            grouped_words.append(word)
        elif (start_time - group_end <= merge_threshold) and (len(grouped_words) < max_group_words):
            # Merge this word into the current group if it doesn't exceed max_group_words
            grouped_words.append(word)
        else:
            # Finish the current group and start a new one
            commit_group()
            group_start = start_time
            grouped_words.append(word)

        group_end = end_time  # Always update the end time to the current word's end time

    # Commit the last group if any
    commit_group()

    return srt_output

def whisper_transcription(audio_file, api_key):
    client = OpenAI(api_key=api_key)
    try:
        with open(audio_file, "rb") as file:
            transcript = client.audio.transcriptions.create(
                file=file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        return transcript.words
    except FileNotFoundError:
        print(f"File not found: {audio_file}")
        raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def generate_srt(input_audio_file, output_srt_file, api_key):
    try:
        words = whisper_transcription(input_audio_file, api_key)
        srt_content = convert_to_srt(words)
        with open(output_srt_file, 'w', encoding='utf-8') as file:
            file.write(srt_content)
        print(f"Subtitles have been saved to {output_srt_file}")
    except Exception as e:
        print(f"Transcription failed: {str(e)}")
