import speech_recognition as sr
from pydub import AudioSegment
from pdfminer.high_level import extract_text
from PIL import Image
from gtts import gTTS
import pytesseract
import os

def text_to_speech(text, output_path):
    """
    Converts text to speech using Google Text-to-Speech API.

    Args:
    - text: A string containing the text to be converted.
    - output_path: A string representing the path to save the output audio file.
    """
    tts = gTTS(text, lang='en')
    tts.save(output_path)

def speech_to_text(file_path):
    """
    Converts speech from an audio file to text using Google Speech Recognition API.

    Args:
    - file_path: A string representing the path of the audio file.

    Returns:
    - A string containing the transcribed text from the audio file.
    """
    return audio_to_text(file_path)  # This function is already defined in your script


def audio_to_text(file_path):
    """
    Converts audio files to text using Google Speech Recognition API.

    Args:
    - file_path: A string representing the path of the audio file.

    Returns:
    - A string containing the transcribed text from the audio file.
    """
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)

    with audio_file as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data)

    return text


def video_to_text(file_path):
    """
    Extracts audio from video files and converts it to text using Google Speech Recognition API.

    Args:
    - file_path: A string representing the path of the video file.

    Returns:
    - A string containing the transcribed text from the video file.
    """
    # Replace 'input_video.mp4' with the actual video file path
    video = AudioSegment.from_file(file_path, "mp4")
    video.export("temp_audio.wav", format="wav")

    text = audio_to_text("temp_audio.wav")

    return text


def pdf_to_text(file_path):
    """
    Extracts text from PDF files.

    Args:
    - file_path: A string representing the path of the PDF file.

    Returns:
    - A string containing the extracted text from the PDF file.
    """
    text = extract_text(file_path)
    return text


def image_to_text(file_path):
    """
    Extracts text from image files using Tesseract OCR.

    Args:
    - file_path: A string representing the path of the image file.

    Returns:
    - A string containing the extracted text from the image file.
    """
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text


def convert_file(input_path, output_path):
    """
    Converts various file types to text using appropriate functions.

    Args:
    - input_path: A string representing the path of the input file.
    - output_path: A string representing the path of the output file (optional).

    Returns:
    - A string containing the extracted or transcribed text from the input file.
    """
    # Determine the file type based on the extension
    file_extension = os.path.splitext(input_path)[1].lower()

    # Call the appropriate function based on the file type
    if file_extension in ['.wav', '.mp3', '.m4a', '.ogg']:
        text = audio_to_text(input_path)
    elif file_extension in ['.mp4', '.avi', '.mkv', '.mov']:
        text = video_to_text(input_path)
    elif file_extension == '.pdf':
        text = pdf_to_text(input_path)
    elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
        text = image_to_text(input_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    if output_path is not None:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

    return text