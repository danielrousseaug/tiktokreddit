# Reddit-TikTok Video Generator

## Overview
This project automates the creation of Reddit-style TikTok videos, where an AI narrator reads a Reddit post while synchronized text appears on the screen, accompanied by a background video. The final product is a short-form, TikTok-style video generated with optimized rendering techniques.

## How It Works
1. **Fetch Reddit Post**: The script retrieves posts from Reddit using the Reddit API.
2. **Determine Narrator Voice**: A local Meta LLM (via Ollama) predicts whether the post author is male or female, selecting an appropriate voice.
3. **Generate Narration**: The post is converted to speech using either Amazon Polly (S3) or 11 Labs for higher-quality narration.
4. **Generate Subtitles**: The narrated MP3 file is transcribed into an SRT subtitle file using OpenAI's Whisper API.
5. **Assemble Video**:
   - Background video is selected.
   - Text animations synchronize with narration.
   - The final video is rendered using FFmpeg (previously MoviePy, but switched for better performance).
6. **Output**: A polished TikTok-style video ready for sharing.

## Features
- **Automated Workflow**: Fully integrates APIs to automate video creation.
- **Voice Selection by AI**: Uses local LLM (Meta via Ollama) to determine an appropriate voice.
- **Optimized Rendering**: Uses raw FFmpeg for faster video production.
- **Accurate Subtitles**: Whisper API ensures high-quality transcriptions.
- **Customizable Voices**: Supports both Amazon Polly and 11 Labs voices.

## File Structure
```
├── config/              # API keys and settings
├── fetch_reddit.py      # Fetches Reddit posts
├── generate_voice.py    # Handles text-to-speech conversion
├── transcribe_audio.py  # Generates subtitles using Whisper
├── video_assembly.py    # Synchronizes text, narration, and background video
├── render_video.py      # FFmpeg-based video rendering
├── utils/               # Helper functions
└── README.md            # Project documentation
```

## Sample Output
Below is an example of an auto-generated Reddit-TikTok video (quality lowered due to upload limites):

https://github.com/user-attachments/assets/355984c2-1f70-4b9e-ae81-478fdc668071

## Installation & Usage
### Prerequisites
- Python 3.8+
- FFmpeg
- OpenAI API access
- Reddit API credentials
- AWS credentials for Polly
- 11 Labs API access
- Ollama for local LLM processing

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/Reddit-TikTok-Generator.git
cd Reddit-TikTok-Generator

# Install dependencies
pip install -r requirements.txt
```

### Running the Script
```bash
python render_video.py
```

## Future Improvements
- **Expand Voice Customization**: Add more nuanced voice selection using LLM-based sentiment analysis.
- **Better Background Video Selection**: Dynamically match background videos based on post content.
- **Faster Processing**: Optimize subtitle timing and rendering for lower latency.

## Contributors
- **Daniel Rousseau** - Project Creator

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
