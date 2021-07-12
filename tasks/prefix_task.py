# prefix_task.py
# by Preston Hager

async def prefix_task(message, self, prefix, add):
    if add:
        message.edit(content=f"Successfully modified the prefix! Use `{prefix}` whenever sending a KBB command.")
        await message.resend()

__all__ = ["prefix_task"]
