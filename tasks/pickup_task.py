# pickup_task.py
# by Preston Hager

async def pickup_task(message, self, author, amount):
    self._add_hearts(author, amount)
    earned_hearts = int(message.content.split('\n')[-1].split(' ')[-1])
    message.edit(content='\n'.join(message.content.split('\n')[:-1]) + f"\nEarned ❤️: {earned_hearts + amount}")
    await message.resend()
    return False

__all__ = ["pickup_task"]
