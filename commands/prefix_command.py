# prefix_command.py
# by Preston Hager

import bot_utils as bot
from tasks import prefix_task

def prefix_command(self, message):
    prefix = ';'
    conditions = [
        bot.TaskCondition("✅", prefix_task, self, prefix, True)
        bot.TaskCondition("❌", prefix_task, self, prefix, False)
    ]
    message = bot.Message("Prefix", message.author, f"Are you sure you want to change the prefix to {prefix}?", task=bot.Task(conditions, [message.author.id], whitelist=True, expires=25.0))
    return message

__all__ = ["prefix_command"]
