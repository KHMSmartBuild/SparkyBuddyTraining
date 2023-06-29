
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import cv2
import numpy as np
import subprocess
from PyQt5.QtWidgets import QApplication,QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
from utils.Prep.you_tube.transcribe_video import transcribe_video
import youtube_dl


class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path

    def get_frame(self, frame_num):
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return frame
        else:
            return None

    def get_frame_count(self):
        cap = cv2.VideoCapture(self.video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        return frame_count

    def get_duration(self):
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', self.video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration = float(result.stdout)
        return duration

    def get_fps(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return fps

    def get_frames(self, start_frame=0, end_frame=None):
        if end_frame is None:
            end_frame = self.get_frame_count() - 1
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        frames = []
        for i in range(start_frame, end_frame + 1):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames

    def get_audio(self, start_time=0, end_time=None):
        if end_time is None:
            duration = self.get_duration()
            end_time = duration - start_time
        result = subprocess.run(['ffmpeg', '-i', self.video_path, '-ss', str(start_time), '-t', str(end_time), '-ac', '2', '-f', 'wav', '-'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        audio = np.frombuffer(result.stdout, dtype=np.int16)
        return audio

# ... Other imports ...

class VideoProcessorGUI(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.path_label = QLabel("Video URL:")
        layout.addWidget(self.path_label)

        self.path_input = QLineEdit()
        layout.addWidget(self.path_input)

        self.process_button = QPushButton("Process Video")
        self.process_button.clicked.connect(self.process_video)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def download_video(self, url):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': 'downloaded_videos/%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            video_path = ydl.prepare_filename(info)
            video = cv2.VideoCapture(video_path)
            return video_path

    def process_video(self):
        video_url = self.path_input.text()
        video_path = self.download_video(video_url)

        if video_path is not None:
            video_processor = VideoProcessor(video_path)

            # Perform desired video processing operations here using the video_processor instance

            # Transcribe the video
            transcription = transcribe_video(video_path)
            print(transcription)
        else:
            print("Error: Video download failed.")

app = QApplication(sys.argv)
gui = VideoProcessorGUI()
gui.show()
sys.exit(app.exec_())
