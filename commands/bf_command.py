# bf_command.py
# by Preston Hager

import datetime
import dateutil

import bot_utils as bot

def bf_command(self, message):
    # Get the user and the available people in the user's guild.
    user = self.database.get_user(int(message.author.id))
    people = self.guilds.get_guild(int(message.guild.id))["people"]
    pool = [p for p in people if p['type'] == 'bf']
    if len(pool) == 0:
        return bot.Message("Boyfriend", message.author, "I'm out of boyfriends!")
    elif user != None and user['relationships']['current'] != {}:
        date_picked = dateutil.parser.parse(user['relationships']['current']['date_picked'])
        if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
            return bot.Message("Boyfriend", message.author, "You already have a relationship, you can't have another right now.")
    boyfriend = self.draw_relationship(message.author.id, message.guild.id, pool)
    return bot.Message("Boyfriend", message.author, f"You have **{boyfriend['name']}**!\nEnjoy your time together!", image_path=f"https://media.githubusercontent.com/media/PrestonHager/KBB/main/images/{boyfriend['image']}")

__all__ = ["bf_command"]
