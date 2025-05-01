import whisper
from moviepy import VideoFileClip
from tempfile import NamedTemporaryFile
from os import path
from error import error_message
import logging
from error import LogicalStack

logger = logging.getLogger(__name__)
WHISPER_MODEL = {
        "small": "tiny";
        "medium": "medium";
        "large": "large-v3"
        }


class Transcription:
    def __init__(self, model="small"):
        "initialising whisper model to be used"
        logger.debug("initialising")

        model_name = WHISPER_MODEL[model]

        self.model_str = model_name

        try:
            self.model = whisper.load_model(model_name)
        except Exception as e:
            logger.error(f"Model failed to initialise:\n{e}")
            return None
        
    def trans_audio(self, audio_file):
        """takes audio file as input and outputs transcription"""
        logger.debug("transcribing audio")

        # check whether inputted audio file exists
        if not path.isfile(audio_file):
            logger.error("Audio file not found")
            return None

        # running the transcription on the audio file (and printing the exception if it fails)
        try:
            result = self.model.transcribe(audio_file, fp16=False)
        except Exception as e:
            logger.error(f"Transcription failed:\n{e}")
            return None

        return result

    def trans_video(self, video_file):
        """takes video file as input and outputs audio transcription dict"""
        logger.debug("transcribing video")

        # set up a temporary audio file
        temp_audio_file = NamedTemporaryFile(suffix=".mp3")

        # check whether inputted video file exists
        if not path.isfile(video_file):
            logger.error("Video file not found")
            return None

        # open video file and write audio to temp file
        try:
            video = VideoFileClip(video_file)
            audio = video.audio
            audio.write_audiofile(temp_audio_file.name)
        except Exception as e:
            logger.error(f"failed to write audio to temp file:\n{e}")
            return None

        # close files
        video.close()
        audio.close()

        # transcribe the audio
        result = self.trans_audio(temp_audio_file.name)

        return result
    

if __name__ == "__main__":
    transcriber = Transcription()

    # result_dict = transcriber.trans_audio("harvard.wav")
    result_dict = transcriber.trans_audio("text_file.txt")
    if result_dict != None:
        segments = [{"id":x["id"],"start":x["start"],"end":x["end"],"text":x["text"]} for x in result_dict["segments"]]
        print(segments)

    result_dict = transcriber.trans_video("sample_video.mp4")
    print(result_dict)
