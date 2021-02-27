# marry_task.py
# by Preston Hager

import random
import threading

async def marry_task(message, main, user_relationships, person, chance, hearts):
    roll = random.random()
    user_relationships[person['name']]['hearts'] -= hearts
    if roll <= chance:
        user_relationships[person['name']]['married'] = True
        save_thread = threading.Thread(target=main._save)
        save_thread.start()
        message.edit(content=f"Successfully married! You are now married to {person['name']}!")
        await message.resend()
    else:
        message.edit(content=f"{person['name']} rejected you, better luck next time.")
        await message.resend()
    return True

__all__ = ["marry_task"]
