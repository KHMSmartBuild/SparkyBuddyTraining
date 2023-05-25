"""
This script transcribes a video file using the Google Cloud Speech-to-Text API. The script loads the necessary libraries and environment variables, defines a function to transcribe the video file, and sends the audio object and configuration options to the Google Cloud Speech-to-Text API for transcription. The transcription results are returned as a list of strings and tuples containing the transcribed text and word time offsets.

Required Libraries:
- io
- os
- google.cloud
- dotenv

Required Environment Variables:
- GOOGLE_API_KEY: Google Cloud credentials for the Speech-to-Text API

Usage:
- Pass the path of the video file to the transcribe_video function to get the transcription results.
"""

import io
import sys
import os
from google.cloud import speech_v1p1beta1 as speech
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define function to transcribe a video file
def transcribe_video(video_file):
    """
    Transcribes a video file using the Google Cloud Speech-to-Text API.

    Args:
    - video_file: A string representing the path of the video file to be transcribed.

    Returns:
    - A list of strings and tuples containing the transcribed text and word time offsets.
    """
    # Create client for Google Cloud Speech-to-Text API
    client = speech.SpeechClient()

    # Set configuration options for the audio file
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True
    )

    # Read the contents of the video file into memory
    with io.open(video_file, 'rb') as file:
        content = file.read()

    # Create audio object from the video file content
    audio = speech.types.RecognitionAudio(content=content)

    # Get the Google Cloud credentials from the environment variables
    credentials = os.getenv('GOOGLE_API_KEY')

    # Set the environment variable for the Google Cloud credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials

    # Send the audio object and configuration options to the Google Cloud Speech-to-Text API for transcription
    response = client.recognize(config=config, audio=audio)

    # Create empty list to store transcription results
    transcript = []

    # Iterate through each result in the response and extract the transcribed text and word time offsets
    for result in response.results:
        transcript.append(result.alternatives[0].transcript)
        for word in result.alternatives[0].words:
            start_time = word.start_time.total_seconds()
            end_time = word.end_time.total_seconds()
            word_text = word.word
            transcript.append((start_time, end_time, word_text))

    # Return the transcription results as a list of strings and tuples
    return transcript

if __name__ == "__main__":
    video_url = sys.argv[1]
    transcription = transcribe_video(video_url)
    with open("transcription.txt", "w") as f:
        f.write(transcription)