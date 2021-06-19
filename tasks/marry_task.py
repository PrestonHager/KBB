# marry_task.py
# by Preston Hager

import random

async def marry_task(message, main, user_id, user_relationships, person, chance, hearts):
    roll = random.random()
    user_relationships[person['name']]['hearts'] -= hearts
    if roll <= chance:
        user_relationships[person['name']]['married'] = True
        message.edit(content=f"Successfully married! You are now married to {person['name']}!")
        await message.resend()
    else:
        message.edit(content=f"{person['name']} rejected you, better luck next time.")
        await message.resend()
    main.database.put_user(user_id, relationships=user_relationships)
    return True

__all__ = ["marry_task"]
