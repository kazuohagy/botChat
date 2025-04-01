import requests
import time
import os
from pytube import YouTube
from googleapiclient.discovery import build
from playsound import playsound

youtube_api_key = "SUA_API_KEY"
channel_id = "SEU_CHANNEL_ID"

def get_live_chat_id():
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.search().list(part='id', channelId=channel_id, eventType='live', type='video')
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        live_chat = youtube.videos().list(part='liveStreamingDetails', id=video_id).execute()
        return live_chat['items'][0]['liveStreamingDetails']['activeLiveChatId']
    return None

def get_chat_messages(live_chat_id):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.liveChatMessages().list(liveChatId=live_chat_id, part='snippet,authorDetails')
    response = request.execute()
    messages = []
    for item in response['items']:
        message = item['snippet']['displayMessage']
        messages.append(message)
    return messages

def send_to_fakeyou(text):
    url = "https://api.fakeyou.com/tts"
    data = {"voice": "neymar_brazil", "text": text}  # Troque "neymar_brazil" para "jair_bolsonaro" se quiser
    response = requests.post(url, json=data)
    if response.status_code == 200:
        audio_url = response.json()["audio_url"]
        audio_path = "audio.mp3"
        with open(audio_path, "wb") as f:
            f.write(requests.get(audio_url).content)
        return audio_path
    return None

def play_audio(file_path):
    playsound(file_path)
    os.remove(file_path)

if __name__ == "__main__":
    live_chat_id = get_live_chat_id()
    if live_chat_id:
        while True:
            messages = get_chat_messages(live_chat_id)
            for msg in messages:
                audio_file = send_to_fakeyou(msg)
                if audio_file:
                    play_audio(audio_file)
            time.sleep(5)
