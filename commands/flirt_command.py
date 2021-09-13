# flirt_command.py
# by Preston Hager

import datetime
import dateutil
import random

import bot_utils as bot

def flirt_command(self, message):
    user = self.database.get_user(int(message.author.id))
    if user != None and user['relationships']['current'] != {}:
        user_relationships = user['relationships']
        person = user_relationships['current']
        last_flirt = dateutil.parser.parse(user_relationships[person['name']]['last_flirt'])
        if (datetime.datetime.now() - last_flirt).total_seconds() < 60 * 2:
            return bot.Message("Flirt", message.author, "You must wait at least 2 minutes between flirts.")
        user_relationships[person['name']]['last_flirt'] = datetime.datetime.now().isoformat()
        self.database.put_user(int(message.author.id), relationships=user_relationships)
        hearts = int(random.random() * 3)
        if hearts < 1:
            return bot.Message("Flirt", message.author, "You didn't gain any ❤️. Better luck next time.")
        else:
            person = user_relationships['current']
            self._add_hearts(message.author, hearts)
            return bot.Message("Flirt", message.author, f"You gained {hearts} ❤️ with {person['name']}!")
    else:
        return bot.Message("Flirt", message.author, "You must be in a relationship to do this.")

__all__ = ["flirt_command"]
