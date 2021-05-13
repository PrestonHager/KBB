# pickup_command.py
# by Preston Hager

import bot_utils as bot
from tasks import pickup_task

def pickup_command(self, message):
    command = message.content[len(self.command_start):].strip().lower().split()
    pickup_line = ' '.join(command[1:])
    if str(message.author.id) in self.relationships and 'current' in self.relationships[str(message.author.id)]:
        name = message.author.nick if message.author.nick != None else message.author.name
        conditions = [
            bot.TaskCondition("❤️", pickup_task, self, message.author, amount=3),
            bot.TaskCondition("✅", pickup_task, self, message.author, amount=2),
            bot.TaskCondition("❌", pickup_task, self, message.author, amount=0)
        ]
        message = bot.Message("Pickup", message.author, f"Rate {name}'s pickup line: **\"{pickup_line}\"**\n❤️ if you love it, ✅ if it's ok, or ❌ if it's terrible.", task=bot.Task(conditions, [message.author.id], whitelist=False, expires=60.0))
        return message
    else:
        return bot.Message("Pickup", message.author, "You must be in a relationship to do this.")

__all__ = ["pickup_command"]
