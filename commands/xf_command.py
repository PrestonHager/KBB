# xf_command.py
# by Preston Hager

import datetime

import bot_utils as bot

def xf_command(self, message):
    # Get the user and the available people in the user's guild.
    user = self.database.get_user(int(message.author.id))
    people = self.guilds.get_guild(int(message.guild.id))["people"]
    if len(self.saved['available']) == 0:
        return bot.Message("Relationship", message.author, "I'm out of people!")
    elif user != None and user['relationships']['current'] != {}:
        date_picked = datetime.datetime.fromisoformat(user['relationships']['current']['date_picked'])
        if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
            return bot.Message("Relationship", message.author, "You already have a relationship, you can't have another right now.")
    xfriend = self.draw_relationship(message.author.id, message.guild.id, people)
    return bot.Message("Relationship", message.author, f"You have **{xfriend['name']}**!\nEnjoy your time together!", image_path=f"images/{xfriend['image']}")

__all__ = ["xf_command"]
