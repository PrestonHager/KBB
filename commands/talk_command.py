# talk_command.py
# by Preston Hager

import random

import bot_utils as bot

def talk_command(self, message):
    command = message.content[len(self.command_start(message.guild.id)):].strip().lower().split()
    user = self.database.get_user(int(message.author.id))
    if user != None and user['relationships']['current'] != {}:
        person = user['relationships']['current']
        if len(command) > 1 and command[1] in self.talking_lines:
            line = random.choice(self.talking_lines[command[1]])
        else:
            line = random.choice(self.talking_lines['sweet'])
        return bot.Message("Talk", message.author, f"{person['name']} says \"{line}\"")
    else:
        return bot.Message("Talk", message.author, "You must be in a relationship to do this.")

__all__ = ["talk_command"]
