# Script name: YT_aud_CL_PR.py
# location = data\raw_data\tools\YT_aud_CL_PR.py
# accessable from Libraries = yes

import os
import openai
import youtube_dl
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

class YouTubeAudioProcessor:
    def download_youtube_audio(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio.wav',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def transcribe_audio_file(self, file_path):
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

    def clean_transcript(self, transcript):
        cleaned_transcript = []
        for result in transcript.results:
            text = result.alternatives[0].transcript.strip()
            cleaned_transcript.append(text)
        return cleaned_transcript

    def generate_documents(self, transcript, user_instructions):
        prompt = f"{user_instructions}\n\nTranscript:\n{transcript}\n\nGenerated Document:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        generated_document = response.choices[0].text.strip()
        return generated_document

    def process_youtube_audio(self, youtube_url, user_instructions):
        self.download_youtube_audio(youtube_url)
        audio_file = "audio.wav"
        transcript = self.transcribe_audio_file(audio_file)
        cleaned_transcript = self.clean_transcript(transcript)
        generated_document = self.generate_documents(cleaned_transcript, user_instructions)
        return generated_document

if __name__ == '__main__':
    youtube_url = input("Enter YouTube URL: ")
    user_instructions = input("Enter user instructions: ")

    processor = YouTubeAudioProcessor()
    generated_document = processor.process_youtube_audio(youtube_url, user_instructions)
    print(f"Generated Document: {generated_document}")
