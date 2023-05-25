# Script name: Whisper_tools.py
# location = gui\Sparky\Whisper_tools.py
# accessable from Libraries = yes
# Author: KHM Smartbuild
# Purpose: TODO add this purpose
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild

import os
import wave
import pyaudio
import openai
import pandas as pd

from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QObject

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class AudioTranscription:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def transcribe(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 16000  # Update the sample rate to 16kHz to match the Whisper ASR requirement

        p = pyaudio.PyAudio()

        wf = wave.open(self.audio_file, 'rb')

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        print("* playing")

        data = wf.readframes(CHUNK)

        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        print("* done playing")

        stream.stop_stream()
        stream.close()

        p.terminate()

        audio_data = open(self.audio_file, 'rb').read()
        response = openai.Audio.transcriptions.create(
            engine="whisper-1",
            audio=audio_data,
            sample_rate=RATE,
            max_tokens=100,
            num_attempts=2,
        )

        return response.choices[0].text

class TrainingDataGenerator:
    def __init__(self, data):
        self.data = data

    def generate_training_data(self):
        data = self.data.drop_duplicates()

        data = data.apply(openai.Completion.create(engine="content-filter-alpha-2", prompt=(data["goal"] + " " + data["sub-goal"])))

        augmented_data = pd.concat([data, data.apply(data["goal"][::-1] + data["sub-goal"][::-1])])

        train_data = augmented_data.sample(frac=0.8, random_state=42)
        val_data = augmented_data.drop(train_data.index).sample(frac=0.5, random_state=42)
        test_data = augmented_data.drop(train_data.index).drop(val_data.index)

        model = openai.Model.list()[0]
        response = model.train(
            examples=train_data.to_dict('records'),
            validation_set=val_data.to_dict('records'),
            test_set=test_data.to_dict('records'),
            model_name_or_id=model.id,
            max_epochs=10,
            n_cpus=4,
            batch_size=32,
            learning_rate=1e-5,
        )

        return response
    
class RealTimeTranscription(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.transcription_label = QLabel()
        self.layout.addWidget(self.transcription_label)

        self.record_audio = RecordAudio()
        self.record_audio.transcribed_text.connect(self.update_transcription_label)
        self.layout.addWidget(self.record_audio)

        self.transcription = ""

    def update_transcription_label(self, text):
        self.transcription += text
        self.transcription_label.setText(self.transcription)

class RecordAudio(QWidget):
    transcribed_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.record_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_recording)
        self.layout.addWidget(self.stop_button)

        self.recording = False

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.record_button.setEnabled(False)
            self._record_audio()

    def stop_recording(self):
        if self.recording:
            self.recording = False

    def _record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 16000  # Update the sample rate to 16kHz to match the Whisper ASR requirement
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        while self.recording:
            data = stream.read(CHUNK)
            frames.append(data)
            QApplication.processEvents()

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        transcript = self.transcribe_audio(frames, RATE)
        print(f"Transcript: {transcript}")
        self.transcribed_text.emit(transcript)

    def transcribe_audio(self, frames, sample_rate):
        audio_data = b''.join(frames)
        response = openai.audio.transcriptions.create(
            engine="whisper-1",
            audio=audio_data,
            sample_rate=sample_rate,
            max_tokens=100,
            num_attempts=2,
        )

        return response.choices[0].text
