# items_command.py
# by Preston Hager

import bot_utils as bot

def items_command(self, message):
    user = self.database.get_user(int(message.author.id))
    if user != None:
        item_fields = bot.MessageFields()
        number = 1
        for i in user['inventory']:
            item = user['inventory'][i]
            item_name = f"{number}) {item['name']}" if item['amount'] == 1 else f"{number}) {item['name']} × {item['amount']}"
            item_fields.add_field((item_name, f"  - {item['description']}"))
            number += 1
        return bot.Message("Inventory", message.author, "", fields=item_fields)
    self.database.new_user(int(message.author.id))
    return bot.Message("Inventory", message.author, f"You have nothing in your inventory!")

__all__ = ["items_command"]
