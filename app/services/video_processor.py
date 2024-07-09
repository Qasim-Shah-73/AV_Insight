import cv2
import os
import shutil
import logging
import traceback
from typing import List
from pathlib import Path
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_images(video_path: str, output_folder: str, interval: int = 15) -> None:
    """
    Extract images from a video at specified intervals.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Path to the output folder for extracted images.
        interval (int): Interval (in seconds) between extracted frames.
    """
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval)
        frame_count = 0
        
        with tqdm(desc="Extracting images", unit="frame") as pbar:
            while True:
                success, image = cap.read()
                if not success:
                    break
                
                if frame_count % frame_interval == 0:
                    image_path = output_path / f"frame_{frame_count:06d}.jpg"
                    cv2.imwrite(str(image_path), image)
                
                frame_count += 1
                pbar.update(1)
    finally:
        cap.release()

def extract_audio(video_path: str, audio_path: str) -> None:
    """
    Extract audio from a video file.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to save the extracted audio file.
    """
    try:
        _, file_extension = os.path.splitext(video_path)
        if file_extension.lower() != '.mkv':
            logger.warning(f"Input file is not MKV. Attempting to process {file_extension} file.")
        
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_path)
        logger.info(f"Audio successfully extracted to {audio_path}")
    except Exception as e:
        logger.error(f"Error extracting audio: {e}")
        raise

def audio_to_text(audio_path: str, chunk_length_ms: int = 60000) -> str:
    """
    Convert audio to text using speech recognition.

    Args:
        audio_path (str): Path to the input audio file.
        chunk_length_ms (int): Length of each audio chunk in milliseconds.

    Returns:
        str: Transcribed text from the audio.
    """
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    transcript = []
    for i, chunk in enumerate(tqdm(chunks, desc="Transcribing audio")):
        chunk_path = f"chunk_{i:03d}.wav"
        chunk.export(chunk_path, format="wav")
        
        try:
            with sr.AudioFile(chunk_path) as source:
                audio_listened = recognizer.record(source)
                text = recognizer.recognize_google(audio_listened)
                transcript.append(text)
        except sr.UnknownValueError:
            logger.warning(f"Chunk {i} could not be understood")
        except sr.RequestError as e:
            logger.error(f"Could not request results for chunk {i}: {e}")
        finally:
            os.remove(chunk_path)
    
    return " ".join(transcript)

    
def get_next_video_folder(base_path='uploads'):
    """
    Determine the next available video folder name.
    """
    os.makedirs(base_path, exist_ok=True)
    existing_folders = [f for f in os.listdir(base_path) if f.startswith('video') and f[5:].isdigit()]
    if not existing_folders:
        return os.path.join(base_path, 'video1')
    last_number = max(int(f[5:]) for f in existing_folders)
    return os.path.join(base_path, f'video{last_number + 1}')

def process_video(video_path: str) -> dict:
    """
    Process the video: extract images, audio, transcribe, and organize output.

    Args:
        video_path (str): Path to the input video file.

    Returns:
        dict: Paths to the output files.
    """
    video_output_folder = get_next_video_folder()
    images_folder = os.path.join(video_output_folder, "images")
    transcript_path = os.path.join(video_output_folder, "transcript.txt")
    temp_audio_path = os.path.join(video_output_folder, "temp_audio.wav")

    os.makedirs(images_folder, exist_ok=True)

    try:
        logger.info(f"Starting video processing for {video_path}")
        
        extract_images(video_path, images_folder)
        logger.info("Image extraction completed")
        
        extract_audio(video_path, temp_audio_path)
        logger.info("Audio extraction completed")
        
        transcript = audio_to_text(temp_audio_path)
        logger.info("Transcription completed")
        
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        logger.info(f"Transcript saved to {transcript_path}")
        
        # Remove the temporary audio file
        os.remove(temp_audio_path)
        logger.info("Temporary audio file removed")
        
        return {
            "video_folder": video_output_folder,
            "images_folder": images_folder,
            "transcript_path": transcript_path
        }

    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")
        logger.error(traceback.format_exc())
        # Clean up the output folder if an error occurred
        shutil.rmtree(video_output_folder, ignore_errors=True)
        raise

    finally:
        # Ensure temporary audio file is removed even if an exception occurs
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    # This block only runs if the script is executed directly
    VIDEO_PATH = os.getenv("VIDEO_PATH", r"C:\Users\Lenovo\Videos\2024-01-05 00-13-54.mkv")
    
    try:
        result = process_video(VIDEO_PATH)
        print("Processing completed successfully.")
        print(f"Video folder: {result['video_folder']}")
        print(f"Images saved in: {result['images_folder']}")
        print(f"Transcript saved as: {result['transcript_path']}")
    except Exception as e:
        print(f"An error occurred: {e}")