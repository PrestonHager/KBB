# view_command.py
# by Preston Hager

import bot_utils as bot

def view_command(self, message):
    command = message.content[len(self.command_start):].strip().lower().split()
    if len(command) > 1:
        if len(message.mentions) < 1:
            return bot.Message("View Relationship", message.author, "You must supply either a mention or nothing (for yourself)")
        user_id = str(message.mentions[0].id)
    else:
        user_id = message.author.id
    user = self.database.get_user(int(user_id))
    if user != None and user['relationships']['current'] != {}:
        user_relationships = user['relationships']
        person = user_relationships['current']
        s = 'You are' if user_id == message.author.id else str(message.mentions[0].id) + ' is'
        hearts = user_relationships[person['name']]['hearts']
        married = "Yes" if user_relationships[person['name']]['married'] else "No"
        return bot.Message("View Relationship", message.author, f"{s} with **{person['name']}** right now.", fields=bot.MessageFields(("❤️", f"+**{hearts}**"), ("💍", f"{married}")), image_path=f"images/{person['image']}")
    else:
        s = 'You don\'t' if user == message.author else message.mentions[0].mention + ' doesn\'t'
        return bot.Message("View Relationship", message.author, f"{s} have a relationship yet.")

__all__ = ["view_command"]
