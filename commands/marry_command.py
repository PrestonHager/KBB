# marry_command.py
# by Preston Hager

import datetime
import random
import threading
from math import e

import bot_utils as bot

def marry_command(self, message):
    command = message.content[len(self.command_start):].strip().lower().split()
    if str(message.author) in self.relationships and 'current' in self.relationships[str(message.author)]:
        user_relationships = self.relationships[str(message.author)]
        person = user_relationships['current']
        hearts = user_relationships[person['name']]['hearts']
        married = user_relationships[person['name']]['married']
        if married:
            return bot.Message("Marry", message.author, f"You are already married to {person['name']}!")
        if hearts >= 25:
            if len(command) > 1:
                try:
                    tried_hearts = int(command[1])
                    if tried_hearts > hearts:
                        return bot.Message("Marry", message.author, "You cannot use ❤️ that you don't have!")
                    else:
                        percentage = (1 / (1 + e ** (-tried_hearts / 25 + 1)))
                        chance = random.random()
                        print(f"Per: {percentage}\tChance: {chance}")
                        user_relationships[person['name']]['hearts'] -= tried_hearts
                        if chance <= percentage:
                            user_relationships[person['name']]['married'] = True
                            save_thread = threading.Thread(target=self._save)
                            save_thread.start()
                            return bot.Message("Marry", message.author, f"You are now married to {person['name']}!")
                        else:
                            return bot.Message("Marry", message.author, f"{person['name']} rejected you, better luck next time.")
                    return
                except ValueError:
                    pass
            return bot.Message("Marry", message.author, "Include how many ❤️ you want to put towards the marriage.\nEvery ❤️ increases the chance of marriage. Minimum of 25 ❤️.")
        else:
            return bot.Message("Marry", message.author, f"You don't have enough ❤️ to ask {person['name']} to marry you.")
    else:
        return bot.Message("Marry", message.author, "You must be in a relationship to do this.")

__all__ = ["marry_command"]
