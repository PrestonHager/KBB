# prefix_task.py
# by Preston Hager

async def prefix_task(message, self, prefix, guild_id, add):
    if add:
        del self.cached_guilds[guild_id]
        self.guilds.put_guild(guild_id, prefix=prefix)
        message.edit(content=f"Successfully modified the prefix!\nUse `{prefix}` as a prefix whenever sending a KBB command.")
        await message.resend()
    else:
        message.edit(content=f"Did not modify the prefix. Issue the command again if you wish to change it.")
        await message.resend()
    return True

__all__ = ["prefix_task"]
