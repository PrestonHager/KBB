# bf_command.py
# by Preston Hager

import datetime

import bot_utils as bot

def bf_command(self, message):
    user = self.database.get_user(int(message.author.id))
    if len(self.saved['available']) == 0:
        return bot.Message("Boyfriend", message.author, "I'm out of boyfriends!")
    elif user != None:
        date_picked = datetime.datetime.fromisoformat(user['relationships']['current']['date_picked'])
        if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
            return bot.Message("Boyfriend", message.author, "You already have a relationship, you can't have another right now.")
    boyfriend = self.draw_boyfriend(message.author)
    return bot.Message("Boyfriend", message.author, f"You have **{boyfriend['name']}**!\nEnjoy your time together!", image_path=f"images/{boyfriend['image']}")

__all__ = ["bf_command"]
