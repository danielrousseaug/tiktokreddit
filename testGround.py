import os
import praw
from screenshot import website_screenshot
import random

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="PostFetcher/0.1 by u/ClueRepresentative83",
    username=os.getenv("REDDIT_USERNAME"),
)

subreddit = reddit.subreddit("AmITheAsshole")

# for submission in subreddit.top(time_filter="month", limit=1):
#     print(submission.title)
#     # Output: the submission's title
#     print(submission.score)
#     # Output: the submission's score
#     print(submission.selftext)
#     # Output: the submission's ID
#     print(submission.url)
#     # Output: the URL the submission points to or the submission's URL if it's a self post

from textToSpeechAWS import generate_tts, adjust_speed
from transcription import generate_srt
from makeVideo import create_video_with_subtitles

for submission in subreddit.top(time_filter="month", limit=1):
    url = submission.url
    output_filename = "Capture_" + str( random.randint(0,10000) )+".png"
    website_screenshot(url, output_filename)
    story = """
AITA for telling everyone in the home that I will plate food from now on and clear labeling for leftovers
Not the A-hole
I have three people in the home right now. My daughter that is going to college and my son and his wife that are staying to save money. The issue is with my son and his wife. They eat so much, and frankly it is a concerning amount.

What I usually do before they moved in was make a meal, everyone eats and then pack up leftovers in the fridge. The food is gone by the time I even try to get seconds. Sometimes I make food and my daughter ain’t home and it’s all gone. I make big meals that can easily feed 4-6 people with leftovers sometimes.

For example, I made a pound of spaghetti with meat sauce. I didn’t even get any, I didn’t grab any and was going to eat after I finished some chores. My daughter wasn’t home and those two ate a whole pound of spaghetti.

I had a two layer cake, almost all was there and went to work. The cake was almost gone when I got home. That was less than 8 hours.

My daughter is very frustrated since there is never any cooked food in the home. I have made double batches and that gives leftovers but they don’t last. The next day the leftovers are gone. It is hurting my wallet and I am over it.

I don’t want to charge for groceries since that won’t solve the issue with leftovers. Or if they eat everything before anyone has the chance to eat

So I sat everyone down and told them I will be plating everyone’s food. That leftovers will be split evenly and labeled clearly. If anyone is still hungry then they can buy more food to eat.

I implemented it today,my daughter and I loved it since we could at and have leftovers. They hated it and are still hungry, this started an argument and they think I am a huge jerk
"""
    text = story
    print(text)
    generate_tts(text)
    # Adjust the speed of the generated audio file
    input_file = "assets/audio.mp3"
    output_file = "assets/audio_speed_adjusted.mp3"
    speed = 1.5  # Increase the speed by 50%
    adjust_speed(input_file, output_file, speed)
    
    api_key = os.getenv("OPENAI_API_KEY")
    input_audio_file_path = "assets/audio.mp3"
    output_srt_file_path = "assets/subtitles.srt"
    generate_srt(input_audio_file_path, output_srt_file_path, api_key)
    
    background_video_path = "assets/background.mp4"
    audio_path = "assets/audio.mp3"
    srt_file_path = "assets/subtitles.srt"
    output_video_path = "assets/output_with_subtitles.mp4"
    font_path = "/Users/danielrousseau/Library/Fonts/neometric.otf"

    create_video_with_subtitles(background_video_path, audio_path, srt_file_path, output_video_path, font_path)



