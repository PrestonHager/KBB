# bf_command.py
# by Preston Hager

import datetime

import bot_utils as bot

def bf_command(self, message):
    if len(self.saved['available']) == 0:
        return bot.Message("Boyfriend", message.author, "I'm out of boyfriends!")
    elif str(message.author) in self.relationships:
        date_picked = datetime.datetime.fromisoformat(self.relationships[str(message.author)]['current']['date_picked'])
        if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
            return bot.Message("Boyfriend", message.author, "You already have a relationship, you can't have another right now.")
    boyfriend = self.draw_boyfriend(message.author)
    return bot.Message("Boyfriend", message.author, f"You have **{boyfriend['name']}**!\nEnjoy your time together!", image_path=f"images/{boyfriend['image']}")

__all__ = ["bf_command"]
