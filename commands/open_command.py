# open_command.py
# by Preston Hager

import random
from uuid import uuid4

import bot_utils as bot

def open_command(self, message):
    user = self.database.get_user(int(message.author.id))
    if user != None:
        # find the first mystery box and open it!
        user_inventory = user['inventory']
        for i in user_inventory:
            item = user_inventory[i]
            if item['item'] == "mystery_box":
                item['amount'] -= 1
                if item['amount'] < 1:
                    del user_inventory[i]
                self.database.put_user(int(message.author.id), inventory=user_inventory)
                item_name = self.random_item(common=20, rare=4, ultra=1)
                item = self._add_item(message.author, item_name)
                article = "an" if item['name'][0] in "aeiouy" else "a"
                return bot.Message("Open Box", message.author, f"You got {article} {item['name']} out of the box!")
        return bot.Message("Open Box", message.author, "You don't have a Mystery Box in your inventory! Vote for KBB via the `vote` command and recieve some!")
    self.database.new_user(int(message.author.id))
    return bot.Message("Open Box", message.author, "You don't have a Mystery Box in your inventory!")

__all__ = ["open_command"]
