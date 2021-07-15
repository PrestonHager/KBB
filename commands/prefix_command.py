# prefix_command.py
# by Preston Hager

import bot_utils as bot
from tasks import prefix_task

def prefix_command(self, message):
    command = ''.join(message.content[len(self.command_start(message.guild.id)):]).split(' ')
    if len(command) < 2:
        message = bot.Message("Prefix", message.author, "You must specify a prefix to use. Usage: `;prefix [prefix]`.")
        return message
    # get the guild id for the task
    prefix = command[1]
    guild_id = message.guild.id
    conditions = [
        bot.TaskCondition("✅", prefix_task, self, prefix, guild_id, True),
        bot.TaskCondition("❌", prefix_task, self, prefix, guild_id, False)
    ]
    message = bot.Message("Prefix", message.author, f"Are you sure you want to change the prefix to `{prefix}`?", task=bot.Task(conditions, [message.author.id], whitelist=True, expires=25.0))
    return message

__all__ = ["prefix_command"]
