import whisper
from moviepy import VideoFileClip
from tempfile import NamedTemporaryFile
from os import path
from .logger_config import get_logger
from app import error
import sys

whisper_model = None
logger = get_logger(__name__)

WHISPER_MODEL = {
        "small": "tiny",
        "medium": "medium",
        "large": "large-v3"
        }


# whisper_model = whisper.load_model("medium")

class Transcription:
    def __init__(self, model_size="small"):
        """initialises Transcription class instance"""
        global whisper_model
        logger.debug("initialising Transcription class instance")

        model_name = WHISPER_MODEL[model_size]
        self.model_str = model_name

        logger.info(f"MODEL: {whisper_model}")
        if whisper_model is None:
            logger.info("whisper model not yet initialised. Initialising now")
            try:
                whisper_model = whisper.load_model(model_name)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                error.push_log(f"Unexpected error while loading Whisper model {model_name}", e, sys.exc_info())
                return None
            logger.info("whisper model successfully initialised")
	# except FileNotFoundError:
	#     logger.exception("Model file not found or failed to download")
	#     error.push_error("Model file missing or inaccessible")
        #     return None
	# except RuntimeError:
	#     logger.exception("Runtime error while loading Whisper (e.g., CUDA out of memory)")
	#     error.push_error("Runtime error during model load")
        #     return None
	# except OSError:
	#     logger.exception("OS error during Whisper model load (disk, permissions, etc.)")
	#     error.push_error("OS error during model load")
        #     return None
	# except ImportError:
	#     logger.exception("Missing dependency (e.g., torch or ffmpeg)")
	#     error.push_error("Missing required dependency")
        #     return None
	# except Exception:
	#     logger.exception("Unexpected error while loading Whisper model")
	#     error.push_error("Unexpected error during model loading")
        #     return None

        
    def trans_audio(self, audio_file):
        """takes audio file as input and outputs transcription"""
        global whisper_model
        logger.debug("transcribing audio")

        # check whether inputted audio file exists
        if not path.isfile(audio_file):
            error.push_log("Audio file not found")
            return None

        # running the transcription on the audio file
        try:
            logger.debug("about to transcribe")
            result = whisper_model.transcribe(audio_file, fp16=False)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            error.push_log(f"Transcription of audio file failed", e, sys.exc_info())
            return None

        logger.debug("transcription successful")
        return result

    def trans_video(self, video_file):
        """takes video file as input and outputs audio transcription dict"""
        logger.debug("transcribing video")

        # set up a temporary audio file
        temp_audio_file = NamedTemporaryFile(suffix=".mp3")

        # check whether inputted video file exists
        if not path.isfile(video_file):
            error.push_log("Video file not found")
            return None

        # open video file and write audio to temp file
        try:
            video = VideoFileClip(video_file)
            audio = video.audio
            audio.write_audiofile(temp_audio_file.name)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            error.push_log(f"failed to write audio to temp file:\n{e}", e, sys.exc_info())
            return None

        # close files
        video.close()
        audio.close()

        # transcribe the audio
        result = self.trans_audio(temp_audio_file.name)
        if result == None:  # error handling
            error.push_log("failed to transcribe audio")
            return None

        return result
    

def test():
    transcriber = Transcription()

    # result_dict = transcriber.trans_audio("harvard.wav")
    # result_dict = transcriber.trans_audio("text_file.txt")
    # if result_dict != None:
    #     segments = [{"id":x["id"],"start":x["start"],"end":x["end"],"text":x["text"]} for x in result_dict["segments"]]
    #     print(segments)

    result_dict = transcriber.trans_video("app/sample_video.mp4")
    print(result_dict)



if __name__ == "__main__":
    from app import app
    with app.app_context():
        transcriber = Transcription()

        # result_dict = transcriber.trans_audio("harvard.wav")
        result_dict = transcriber.trans_audio("text_file.txt")
        if result_dict != None:
            segments = [{"id":x["id"],"start":x["start"],"end":x["end"],"text":x["text"]} for x in result_dict["segments"]]
            print(segments)

        result_dict = transcriber.trans_video("sample_video.mp4")
        print(result_dict)
