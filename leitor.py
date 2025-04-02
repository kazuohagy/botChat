import edge_tts
import asyncio
import pytchat
from playsound import playsound
from multiprocessing import Process
#pt-BR-FranciscaNeural audio femenino
#pt-BR-AntonioNeural audio masculino

from googleapiclient.discovery import build
#va no google cloud e cria um projeto, depois ativa a api do youtube e gera uma chave de api
#https://console.cloud.google.com/apis/library/youtube.googleapis.com
#ou se preferir pode apenas colocar na variavel video_id2 o id da live
#e rodar o programa normalmente
API_KEY = ""
CHANNEL_ID = ""

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

live_id = get_live_video_id()
print(f"ID da Live: {live_id}")

video_id2 = live_id  # ID da live por exemplo: "dQw4w9WgXcQ"
nome_arquivo = "audio.mp3"  # Sempre o mesmo arquivo

def tocar_audio(arquivo):
    """Executa o áudio de forma segura sem bloquear o arquivo."""
    playsound(arquivo)

async def texto_para_audio(texto):
    """Gera e toca o áudio, substituindo o arquivo anterior."""
    communicate = edge_tts.Communicate(texto, "pt-BR-FranciscaNeural")
    await communicate.save(nome_arquivo)  # Sempre salva no mesmo arquivo
    print(f"Áudio salvo como {nome_arquivo}")

    # Executa o áudio em um processo separado
    p = Process(target=tocar_audio, args=(nome_arquivo,))
    p.start()
    p.join()  # Aguarda a execução para evitar múltiplas reproduções sobrepostas

if __name__ == '__main__':
    chat = pytchat.create(video_id2)

    while chat.is_alive():
        for msg in chat.get().sync_items():
            print(f"{msg.author.name} mandou 0 reais: {msg.message}")
            asyncio.run(texto_para_audio(f"{msg.author.name} mandou 0 reais: {msg.message}"))