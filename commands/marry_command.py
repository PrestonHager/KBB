# marry_command.py
# by Preston Hager

import datetime
import random
import threading
from math import e

import bot_utils as bot
from tasks import marry_task

def marry_command(self, message):
    command = message.content[len(self.command_start):].strip().lower().split()
    user = self.database.get_user(int(message.author.id))
    if user != None and user['relationships']['current'] != {}:
        user_relationships = user['relationships']
        person = user_relationships['current']
        hearts = user_relationships[person['name']]['hearts']
        married = user_relationships[person['name']]['married']
        if married:
            return bot.Message("Marry", message.author, f"You are already married to {person['name']}!")
        if hearts >= 25:
            if len(command) > 1:
                try:
                    tried_hearts = int(command[1])
                    if tried_hearts < 25:
                        return bot.Message("Marry", message.author, "The minimum number of ❤️ is 25.")
                    elif tried_hearts > hearts:
                        return bot.Message("Marry", message.author, "You cannot use ❤️ that you don't have!")
                    else:
                        chance = (1 / (1 + e ** (-tried_hearts / 25 + 1)))
                        percentage = int(chance * 100)
                        return bot.Message("Marry", message.author, f"Would you like to try to marry {person['name']} using your {tried_hearts} ❤️?\nThere is a {percentage}\% chance of it succeeding.", bot.Task([bot.TaskCondition("✅", marry_task, main=self, user_id=int(message.author.id), user_relationships=user_relationships, person=person, chance=chance, hearts=tried_hearts)], [message.author.id], expires=60.0))
                    return
                except ValueError:
                    pass
            return bot.Message("Marry", message.author, "Include how many ❤️ you want to put towards the marriage.\nEvery ❤️ increases the chance of marriage. Minimum of 25 ❤️.")
        else:
            return bot.Message("Marry", message.author, f"You don't have enough ❤️ to ask {person['name']} to marry you.")
    else:
        return bot.Message("Marry", message.author, "You must be in a relationship to do this.")

__all__ = ["marry_command"]
