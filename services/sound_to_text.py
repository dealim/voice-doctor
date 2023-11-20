# Imports the Google Cloud client library
from google.cloud import speech
import io
import os
from pytube import YouTube

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/GCP-TEAM2/services/appteam02-069a59c45dca.json"

# Instantiates a client
client = speech.SpeechClient()

# 영상 다운
path = '/app/GCP-TEAM2/services/'

# video_url = input("Please enter the video URL: ")
video_url = "https://youtu.be/jznTCqrHoMw"
yt = YouTube(video_url)

#Get highest bitrate audio stream for given codec (defaults to mp4)
audio = yt.streams.get_audio_only()
audio.download(output_path=path)
file_name = audio.default_filename
source = path + file_name

if ' ' in file_name:
    os.rename(source, source.replace(' ', '_'))
    file_name = source.replace(' ','_')

file_without_ext = os.path.splitext(file_name)[0]
command = f"ffmpeg -i {file_name} {file_without_ext}.mp3"
os.system(command)
os.remove(file_name)

# Loads the audio into memory
with io.open(f'{file_without_ext}.mp3', 'rb') as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    sample_rate_hertz=16000,
    language_code='ko-KR')

# Detects speech in the audio file
# response = client.recognize(config, audio)
response = client.recognize(config=config, audio=audio)
print("response : \n",response)
for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))