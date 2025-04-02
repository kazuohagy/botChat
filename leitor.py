import edge_tts
import asyncio
import pytchat
from playsound import playsound
from multiprocessing import Process
#pt-BR-FranciscaNeural audio femenino
#pt-BR-AntonioNeural audio masculino
video_id = "MwEJyxlIhks"  # ID da live
nome_arquivo = "audio.mp3"  # Sempre o mesmo arquivo

def tocar_audio(arquivo):
    """Executa o áudio de forma segura sem bloquear o arquivo."""
    playsound(arquivo)

async def texto_para_audio(texto):
    """Gera e toca o áudio, substituindo o arquivo anterior."""
    communicate = edge_tts.Communicate(texto, "pt-BR-AntonioNeural")
    await communicate.save(nome_arquivo)  # Sempre salva no mesmo arquivo
    print(f"Áudio salvo como {nome_arquivo}")

    # Executa o áudio em um processo separado
    p = Process(target=tocar_audio, args=(nome_arquivo,))
    p.start()
    p.join()  # Aguarda a execução para evitar múltiplas reproduções sobrepostas

if __name__ == '__main__':
    chat = pytchat.create(video_id)

    while chat.is_alive():
        for msg in chat.get().sync_items():
            print(f"{msg.author.name} mandou 0 reais: {msg.message}")
            asyncio.run(texto_para_audio(f"{msg.author.name} mandou 0 reais: {msg.message}"))