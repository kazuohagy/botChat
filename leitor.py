import edge_tts
import asyncio
import pytchat
from playsound import playsound
from multiprocessing import Process
from googleapiclient.discovery import build
import time

API_KEY = ""
CHANNEL_ID = ""
nome_arquivo = "audio.mp3"  # Sempre o mesmo arquivo

def get_live_video_id():
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        part="id",
        channelId=CHANNEL_ID,
        eventType="live",
        type="video"
    )
    response = request.execute()
    
    if "items" in response and len(response["items"]) > 0:
        return response["items"][0]["id"]["videoId"]
    return None

def tocar_audio(arquivo):
    """Executa o áudio de forma segura sem bloquear o arquivo."""
    playsound(arquivo)

async def texto_para_audio(texto):
    """Gera e toca o áudio, substituindo o arquivo anterior."""
    communicate = edge_tts.Communicate(texto, "pt-BR-FranciscaNeural")
    await communicate.save(nome_arquivo)
    print(f"[TTS] Áudio salvo como {nome_arquivo}")

    p = Process(target=tocar_audio, args=(nome_arquivo,))
    p.start()
    p.join()

async def main():
    while True:
        try:
            live_id = get_live_video_id()
            if not live_id:
                print("[INFO] Nenhuma live encontrada. Tentando novamente em 15 segundos...")
                await asyncio.sleep(15)
                continue

            print(f"[INFO] Live detectada. ID: {live_id}")
            chat = pytchat.create(video_id=live_id)

            while chat.is_alive():
                for msg in chat.get().sync_items():
                    texto = f"{msg.author.name} mandou 0 reais: {msg.message}"
                    print(f"[CHAT] {texto}")
                    await texto_para_audio(texto)
        except Exception as e:
            print(f"[ERRO] {e}")
            print("[INFO] Reiniciando em 10 segundos...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
