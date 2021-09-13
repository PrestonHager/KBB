# time_command.py
# by Preston Hager

import datetime
import dateutil

import bot_utils as bot

def time_command(self, message):
    user = self.database.get_user(int(message.author.id))
    if user == None or user['relationships']['current'] == {}:
        return bot.Message("Time Left", message.author, f"Type `;bf`, `;gf`, or `;xf` to get a relationship!")
    user_relationships = user['relationships']
    person = user_relationships['current']
    last_flirt = dateutil.parser.parse(user_relationships[person['name']]['last_flirt'])
    till_next_flirt = datetime.timedelta(seconds=60 * 2 - (datetime.datetime.now() - last_flirt).total_seconds())
    if till_next_flirt < datetime.timedelta(seconds=0):
        flirt_string = "You can flirt with your relationship at any time.\n"
    else:
        formatted_time = self._format_time(till_next_flirt)
        flirt_string = f"You can flirt with your relationship in `{formatted_time}`\n"
    date_picked = dateutil.parser.parse(user_relationships['current']['date_picked'])
    time_remaining = datetime.timedelta(seconds=24 * 60 * 60 - (datetime.datetime.now() - date_picked).total_seconds())
    if time_remaining < datetime.timedelta(seconds=0):
        return bot.Message("Time Left", message.author, f"{flirt_string}You can claim a new relationship at any time.")
    else:
        formatted_time = self._format_time(time_remaining)
        return bot.Message("Time Left", message.author, f"{flirt_string}You have `{formatted_time}` until you can claim a new relationship.")

__all__ = ["time_command"]
