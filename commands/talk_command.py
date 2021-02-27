# talk_command.py
# by Preston Hager

import random

import bot_utils as bot

def talk_command(self, message):
    if str(message.author) in self.relationships and 'current' in self.relationships[str(message.author)]:
        person = self.relationships[str(message.author)]['current']
        line = random.choice(self.talking_lines['dirty'])
        return bot.Message("Talk", message.author, f"{person['name']} says \"{line}\"")
    else:
        return bot.Message("Talk", message.author, "You must be in a relationship to do this.")

__all__ = ["talk_command"]
