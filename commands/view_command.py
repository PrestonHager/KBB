# view_command.py
# by Preston Hager

import bot_utils as bot

def view_command(self, message):
    command = message.content[len(self.command_start):].strip().lower().split()
    if len(command) > 1:
        if len(message.mentions) < 1:
            return bot.Message("View Relationship", message.author, "You must supply either a mention or nothing (for yourself)")
        user = str(message.mentions[0])
    else:
        user = message.author
    if str(user) in self.relationships and 'current' in self.relationships[str(user)]:
        person = self.relationships[str(user)]['current']
        s = 'You are' if user == message.author else message.mentions[0].mention + ' is'
        hearts = self.relationships[str(user)][person['name']]['hearts']
        married = "Yes" if self.relationships[str(user)][person['name']]['married'] else "No"
        return bot.Message("View Relationship", message.author, f"{s} with **{person['name']}** right now.", fields=bot.MessageFields(("❤️", f"+**{hearts}**"), ("💍", f"{married}")), image_path=f"images/{person['image']}")
    else:
        s = 'You don\'t' if user == message.author else message.mentions[0].mention + ' doesn\'t'
        return bot.Message("View Relationship", message.author, f"{s} have a relationship yet.")

__all__ = ["view_command"]
