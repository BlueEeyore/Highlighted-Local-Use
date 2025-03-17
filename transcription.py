import whisper
from moviepy import VideoFileClip


AUDIO_FILENAME = "audio_file.wav"
WHISPER_MODEL = "tiny"


def trans_audio(audio_file):
    """takes audio file as input and outputs transcription"""
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio_file, fp16=False)
    return result["text"]


def trans_video(video_file):
    """takes video file as input and outputs audio transcription"""
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(AUDIO_FILENAME)

    result = trans_audio(AUDIO_FILENAME)

    return result


# print(trans_audio("harvard.wav"))
print(trans_video("sample_video.mp4"))
