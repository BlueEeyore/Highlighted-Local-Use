from faster_whisper import WhisperModel
from moviepy import VideoFileClip
from tempfile import NamedTemporaryFile
from os import path
from .logger_config import get_logger
from app import error
import sys

whisper_model = None
logger = get_logger(__name__)

# Model mapping for faster-whisper
WHISPER_MODEL = {
    "small": "tiny",
    "medium": "small",
    "large": "medium"
}


class Transcription:
    # Track the currently loaded model name as a class attribute
    last_model_name = None

    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        """initialises Transcription class instance using faster-whisper"""
        global whisper_model
        logger.debug("initialising Transcription class instance")

        model_name = WHISPER_MODEL.get(model_size, model_size)
        
        # If a model is loaded but it's different from what's requested, clear it
        if whisper_model is not None and Transcription.last_model_name != model_name:
            logger.info(f"Switching whisper model from {Transcription.last_model_name} to {model_name}")
            whisper_model = None

        if whisper_model is None:
            logger.info(f"faster-whisper model '{model_name}' not yet initialised. Initialising now")
            try:
                # faster-whisper initialization
                whisper_model = WhisperModel(model_name, device=device, compute_type=compute_type)
                Transcription.last_model_name = model_name
            except KeyboardInterrupt:
                raise
            except Exception as e:
                error.push_log(
                    f"Unexpected error while loading faster-whisper model {model_name}",
                    e,
                    sys.exc_info()
                )
                whisper_model = None
                return
            logger.info("faster-whisper model successfully initialised")

    def trans_audio(self, audio_file):
        """takes audio file as input and outputs transcription"""
        global whisper_model
        logger.debug("transcribing audio")

        # check whether inputted audio file exists
        if not path.isfile(audio_file):
            error.push_log("Audio file not found")
            return None

        if whisper_model is None:
            error.push_log("Whisper model is not initialized")
            return None

        # running the transcription on the audio file
        try:
            logger.debug("about to transcribe")
            # faster-whisper returns a generator for segments and an info object
            segments, info = whisper_model.transcribe(
                audio_file,
                beam_size=5,
            )
            
            # Convert segments generator to a list of dicts to match original whisper format
            segments_list = []
            for segment in segments:
                segments_list.append({
                    "id": segment.id,
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                    "tokens": segment.tokens,
                    "temperature": segment.temperature,
                    "avg_logprob": segment.avg_logprob,
                    "compression_ratio": segment.compression_ratio,
                    "no_speech_prob": segment.no_speech_prob
                })
            
            result = {
                "segments": segments_list,
                "language": info.language
            }
            
        except KeyboardInterrupt:
            raise
        except Exception as e:
            error.push_log(
                "Transcription of audio file failed",
                e,
                sys.exc_info()
            )
            return None

        logger.debug("transcription successful")
        return result

    def trans_video(self, video_file):
        """takes video file as input and outputs audio transcription dict"""
        logger.debug("transcribing video")

        # check whether inputted video file exists
        if not path.isfile(video_file):
            error.push_log("Video file not found")
            return None

        # set up a temporary audio file
        temp_audio_file = NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_audio_path = temp_audio_file.name
        temp_audio_file.close()

        # open video file and write audio to temp file
        try:
            video = VideoFileClip(video_file)
            audio = video.audio
            audio.write_audiofile(temp_audio_path, logger=None) # Disable moviepy logging
        except KeyboardInterrupt:
            raise
        except Exception as e:
            error.push_log(
                f"failed to write audio to temp file:\n{e}",
                e,
                sys.exc_info()
            )
            if path.exists(temp_audio_path):
                import os
                os.remove(temp_audio_path)
            return None
        finally:
            if 'video' in locals():
                video.close()
            if 'audio' in locals():
                audio.close()

        # transcribe the audio
        result = self.trans_audio(temp_audio_path)
        
        # Clean up temp file
        import os
        if path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        if result is None:  # error handling
            error.push_log("failed to transcribe audio")
            return None

        return result


def test():
    transcriber = Transcription()
    # Replace with an actual test file path if needed
    # result_dict = transcriber.trans_video("app/sample_video.mp4")
    # print(result_dict)


if __name__ == "__main__":
    # This part might need adjustment depending on how you run it
    transcriber = Transcription()
    # Example usage:
    # result = transcriber.trans_audio("path/to/audio.mp3")
    # print(result)
