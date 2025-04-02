import edge_tts
import asyncio
import pytchat
from playsound import playsound
import time
import os

video_id = "0FARWIfBPps"  # ID da live
chat = pytchat.create(video_id)

async def apagar_audio(nome_arquivo):
    """Aguarda 5 segundos e apaga o arquivo de áudio."""
    await asyncio.sleep(5)  # Aguarda 5 segundos antes de apagar
    if os.path.exists(nome_arquivo):  # Confirma se o arquivo ainda existe
        os.remove(nome_arquivo)
        print(f"Arquivo {nome_arquivo} apagado.")

async def texto_para_audio(texto):
    """Gera, toca e agenda a exclusão do áudio."""
    nome_arquivo = f"audio_{int(time.time())}.mp3"
    communicate = edge_tts.Communicate(texto, "pt-BR-AntonioNeural")
    await communicate.save(nome_arquivo)
    print(f"Áudio salvo como {nome_arquivo}")

    playsound(nome_arquivo)  # Toca o áudio

    # Agenda a exclusão do arquivo após 5 segundos
    asyncio.create_task(apagar_audio(nome_arquivo))

while chat.is_alive():
    for msg in chat.get().sync_items():
        print(f"{msg.author.name}: {msg.message}")
        asyncio.run(texto_para_audio(f"{msg.author.name}: {msg.message}"))
