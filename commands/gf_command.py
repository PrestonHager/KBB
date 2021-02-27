# gf_command.py
# by Preston Hager

import datetime

import bot_utils as bot

def gf_command(self, message):
    if len(self.saved['available']) == 0:
        return bot.Message("Girlfriend", message.author, "I'm out of girlfriends!")
    elif str(message.author) in self.relationships:
        date_picked = datetime.datetime.fromisoformat(self.relationships[str(message.author)]['current']['date_picked'])
        if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
            return bot.Message("Girlfriend", message.author, "You already have a relationship, you can't have another right now.")
    girlfriend = self.draw_girlfriend(message.author)
    return bot.Message("Girlfriend", message.author, f"You have **{girlfriend['name']}**!\nEnjoy your time together!", image_path=f"images/{girlfriend['image']}")

__all__ = ["gf_command"]
