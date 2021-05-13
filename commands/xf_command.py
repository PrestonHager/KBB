# xf_command.py
# by Preston Hager

import datetime

import bot_utils as bot

def xf_command(self, message):
    if len(self.saved['available']) == 0:
        return bot.Message("Relationship", message.author, "I'm out of people!")
    elif str(message.author.id) in self.relationships:
        date_picked = datetime.datetime.fromisoformat(self.relationships[str(message.author.id)]['current']['date_picked'])
        if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
            return bot.Message("Relationship", message.author, "You already have a relationship, you can't have another right now.")
    xfriend = self.draw_relationship(message.author)
    return bot.Message("Relationship", message.author, f"You have **{xfriend['name']}**!\nEnjoy your time together!", image_path=f"images/{xfriend['image']}")

__all__ = ["xf_command"]
