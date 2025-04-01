import pytchat

video_id = "0FARWIfBPps"  # Substitua pelo ID da sua live

chat = pytchat.create(video_id)
while chat.is_alive():
    for msg in chat.get().sync_items():
        print(f"{msg.author.name}: {msg.message}")