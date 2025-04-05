import whisper
from moviepy import VideoFileClip
from tempfile import NamedTemporaryFile


AUDIO_FILENAME = "audio_file.wav"
WHISPER_MODEL = "tiny"


class Transcription:
    def __init__(self, model=WHISPER_MODEL):
        "initialising whisper model to be used"
        self.model_str = whisper_model
        self.model = whisper.load_model(whisper_model)
        
    def trans_audio(self, audio_file):
        """takes audio file as input and outputs transcription"""
        result = self.model.transcribe(audio_file, fp16=False)
        return result

    def trans_video(self, video_file):
        """takes video file as input and outputs audio transcription dict"""
        # set up a temporary audio file
        temp_audio_file = NamedTemporaryFile(suffix=".mp3")

        # open video file and write audio to temp file
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(temp_audio_file.name)

        # close files
        video.close()
        audio.close()

        # transcribe the audio
        result = self.trans_audio(temp_audio_file.name)

        return result
    

if __name__ == "__main__":
    transcriber = Transcription()

    result_dict = transcriber.trans_audio("harvard.wav")
    segments = [{"id":x["id"],"start":x["start"],"end":x["end"],"text":x["text"]} for x in result_dict["segments"]]
    print(segments)

    result_dict = transcriber.trans_video("sample_video.mp4")
    print(result_dict)

