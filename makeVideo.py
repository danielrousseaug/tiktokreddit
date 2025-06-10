from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import os
import re

def create_video_with_subtitles(background_video_path, audio_path, srt_file_path, output_video_path, font_path):
    def split_subtitle_text(text, max_length=15):
        if len(text) <= max_length:
            return text
        else:
            middle_index = len(text) // 2
            before_middle = text.rfind(' ', 0, middle_index)
            after_middle = text.find(' ', middle_index)
            split_index = (before_middle if middle_index - before_middle < after_middle - middle_index else after_middle) or len(text)
            return text[:split_index].rstrip() + '\n' + text[split_index:].lstrip()

    def parse_srt(srt_content):
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n', re.DOTALL)
        subtitles = []
        for match in pattern.finditer(srt_content):
            start, end, text = match.group(2), match.group(3), match.group(4).replace("\n", " ")
            subtitles.append({"start": start, "end": end, "text": text.strip()})
        return subtitles

    def srt_time_to_seconds(time):
        hours, minutes, seconds, milliseconds = map(int, re.split('[:,]', time))
        return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0

    with open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    subtitles = parse_srt(srt_content)

    background_clip = VideoFileClip(background_video_path)
    audio_clip = AudioFileClip(audio_path)

    loop_count = int(audio_clip.duration / background_clip.duration) + 1
    looped_background_clip = concatenate_videoclips([background_clip] * loop_count)

    final_w, final_h = looped_background_clip.size
    target_width = final_h * 9 // 16
    x_center = final_w / 2
    mobile_clip = looped_background_clip.crop(x1=x_center - (target_width / 2), x2=x_center + (target_width / 2))

    final_clip = mobile_clip.set_audio(audio_clip).subclip(0, audio_clip.duration)
    clips = [final_clip]

    for subtitle in subtitles:
        start = srt_time_to_seconds(subtitle["start"])
        end = srt_time_to_seconds(subtitle["end"])
        adjusted_text = split_subtitle_text(subtitle["text"], max_length=15)
        text_clip_variations = [
            {"color": "black", "position_offset": (-2, -2)},
            {"color": "black", "position_offset": (5, 5)},
            {"color": "white", "position_offset": (0, 0)},
        ]
        for variation in text_clip_variations:
            txt_clip = TextClip(adjusted_text, fontsize=64, color=variation["color"], font=font_path)
            txt_width, txt_height = txt_clip.size
            centered_position = ((final_w - txt_width) / 2 + variation["position_offset"][0],
                                 (final_h - txt_height) / 2 + variation["position_offset"][1])
            txt_clip = txt_clip.set_position(centered_position).set_start(start).set_duration(end - start)
            clips.append(txt_clip)

    final_clip_with_subtitles = CompositeVideoClip(clips)
    final_clip_with_subtitles.write_videofile(output_video_path, codec="libx264", preset="slow", bitrate="5000k", audio_codec="aac", fps=60)
    print(f"Video with subtitles saved to {output_video_path}")

# Example usage
# background_video_path = "assets/background.mp4"
# audio_path = "assets/audio.mp3"
# srt_file_path = "assets/subtitles.srt"
# output_video_path = "assets/output_with_subtitles.mp4"
# font_path = "/Users/danielrousseau/Library/Fonts/neometric.otf"

# create_video_with_subtitles(background_video_path, audio_path, srt_file_path, output_video_path, font_path)
