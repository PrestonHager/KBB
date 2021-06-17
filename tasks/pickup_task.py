# pickup_task.py
# by Preston Hager

async def pickup_task(message, self, author, amount):
    self._add_hearts(author, amount)
    return False

__all__ = ["pickup_task"]
