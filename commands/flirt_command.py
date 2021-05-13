# flirt_command.py
# by Preston Hager

import datetime
import random

import bot_utils as bot

def flirt_command(self, message):
    if str(message.author.id) in self.relationships and 'current' in self.relationships[str(message.author.id)]:
        person = self.relationships[str(message.author.id)]['current']
        last_flirt = datetime.datetime.fromisoformat(self.relationships[str(message.author.id)][person['name']]['last_flirt'])
        if (datetime.datetime.now() - last_flirt).total_seconds() < 60 * 2:
            return bot.Message("Flirt", message.author, "You must wait at least 2 minutes between flirts.")
        self.relationships[str(message.author.id)][person['name']]['last_flirt'] = datetime.datetime.now().isoformat()
        hearts = int(random.random() * 3)
        if hearts < 1:
            return bot.Message("Flirt", message.author, "You didn't gain any ❤️. Better luck next time.")
        else:
            person = self.relationships[str(message.author.id)]['current']
            self._add_hearts(message.author, hearts)
            return bot.Message("Flirt", message.author, f"You gained {hearts} ❤️ with {person['name']}!")
    else:
        return bot.Message("Flirt", message.author, "You must be in a relationship to do this.")

__all__ = ["flirt_command"]
