# Script name: Audio_Trans_clean.py
# location = data\raw_data\tools\Audio_Trans_clean.py
# accessable from Libraries = yes
# functions = transcribe_audio_file

import os
import json
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'



def transcribe_audio_file(file_path):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=file_path)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    response = client.recognize(config=config, audio=audio)
    return response

def clean_transcript(transcript):
    cleaned_transcript = []
    for result in transcript.results:
        text = result.alternatives[0].transcript.strip()
        cleaned_transcript.append(text)
    return cleaned_transcript

def convert_to_json(cleaned_transcript, output_file):
    data = [{"task_category": "", "text": text} for text in cleaned_transcript]
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    audio_file = "path/to/your/audio/file.wav"
    output_file = "cleaned_transcript.json"

    # Convert audio file to the required format
    AudioSegment.from_file(audio_file).export("temp.wav", format="wav", parameters=["-ac", "1", "-ar", "16000"])

    # Transcribe audio to text
    transcript = transcribe_audio_file("temp.wav")
    os.remove("temp.wav")

    # Clean the transcript
    cleaned_transcript = clean_transcript(transcript)

    # Convert cleaned transcript to JSON format
    convert_to_json(cleaned_transcript, output_file)
