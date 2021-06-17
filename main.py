# main.py
# by Preston Hager

import discord
import json
import random
import datetime
import threading

import commands
import bot_utils as bot

HELP_MESSAGE = """**;help** - shows this help message
**;bf** - give me a boyfriend
**;gf** - give me a girlfriend
**;view [person]** - view a current relationship
**;flirt** - flirt with your current relationship for hearts
**;marry [hearts]** - ask your relationship to marry you
**;talk** - talk to your relationship
**;time** - how much time until next day"""
COMMANDS = ["time", "bf", "gf", "xf", "view", "flirt", "marry", "talk"]

class KBB(discord.Client):
    command_start = ';'
    saved = {"all": [], "available": []}
    relationships = {}
    available_queue = []
    talking_lines = {}
    tasks = {}

    async def on_ready(self):
        print("Ready and logged on as {}!".format(self.user))
        try:
            with open("save.json", 'r') as f_in:
                self.saved = json.load(f_in)
        except:
            self.saved = {"all": [], "available": []}
        try:
            with open("relationships.json", 'r') as f_in:
                self.relationships = json.load(f_in)
        except:
            self.relationships = {}
        try:
            with open("inventories.json", 'r') as f_in:
                self.inventories = json.load(f_in)
        except:
            self.inventories = {}
        with open("all.csv", 'r') as f_in:
            available = [{"name": l.split(",")[0], "image": l.split(",")[1], "type": l.split(",")[2]} for l in f_in.read().strip().split("\n")[1:]]
        for person in available:
            if person not in self.saved["all"]:
                self.saved["all"].append(person)
                self.saved["available"].append(person)
        save_thread = threading.Thread(target=self._save, args=("saved",))
        save_thread.start()
        with open("texts/dirty.txt", 'r') as f_in:
            self.talking_lines['dirty'] = f_in.read().strip().split('\n')

    async def on_message(self, message):
        if message.content.startswith(self.command_start):
            await self._command(message)

    async def on_reaction_add(self, reaction, user):
        message_id = reaction.message.id
        if message_id in self.tasks.keys():
            succeeded = await self.tasks[message_id].on_reaction_add(reaction, user)
            if succeeded:
                del self.tasks[message_id]

    async def on_user_update(self, before, after):
        # TODO: add a conversion in database for when user changes
        # their username or discriminator.
        pass

    async def _command(self, message):
        command = message.content[len(self.command_start):].strip().lower().split()
        first_word = command[0]
        print(f"Received command `{' '.join(command)}` from {message.author.name}")
        if first_word in COMMANDS:
            message_to_send = commands.command(first_word, self, message)
            await self._send_message(message.channel, message_to_send)
        elif first_word == "help":
            await self._send_message(message.channel, bot.Message("Help", False, HELP_MESSAGE))

    async def _send_message(self, channel, message):
        await message.send(channel)
        if message.task != None:
            self.tasks[message.sent_message.id] = message.create_task()

    def _format_time(self, timedelta):
        hours, remainder = divmod(timedelta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(seconds)}s"
        if minutes > 0:
            formatted_time = f"{int(minutes)}m " + formatted_time
        if hours > 0:
            formatted_time = f"{int(hours)}h " + formatted_time
        return formatted_time

    def draw_boyfriend(self, user):
        pool = [d for d in self.saved['available'] if d['type'] == 'bf']
        return self._draw_relationship_from_pool(user, pool)

    def draw_girlfriend(self, user):
        pool = [d for d in self.saved['available'] if d['type'] == 'gf']
        return self._draw_relationship_from_pool(user, pool)

    def draw_relationship(self, user):
        pool = self.saved['available']
        return self._draw_relationship_from_pool(user, pool)

    def _draw_relationship_from_pool(self, user, pool):
        if str(user) not in self.relationships:
            self.relationships[str(user)] = {}
        else:
            person = self.relationships[str(user)]['current']
            del person['date_picked']
            self.relationships[str(user)][person['name']]['married'] = False
            self.available_queue.append(person)
        user_relationships = self.relationships[str(user)]
        person = random.choice(pool)
        user_relationships['current'] = person
        user_relationships['current']['date_picked'] = datetime.datetime.now().isoformat()
        if person['name'] in user_relationships:
            user_relationships['picked'] += 1
        else:
            user_relationships[person['name']] = {"hearts": 0, "total_time": 0, "picked": 1, "married": False, "last_flirt": (datetime.datetime.now() - datetime.timedelta(minutes=2)).isoformat()}
        self.saved['available'].remove(person)
        if len(self.available_queue) > 0:
            self.saved['available'].append(self.available_queue[-1])
            self.available_queue.pop()
        save_thread = threading.Thread(target=self._save, args=("rs",))
        save_thread.start()
        return person

    def _add_hearts(self, user, amount=1):
        user_relationships = self.relationships[str(user)]
        person = user_relationships['current']
        user_relationships[person['name']]['hearts'] += amount
        save_thread = threading.Thread(target=self._save, args=("relationships",))
        save_thread.start()

    def _add_item(self, user, item):
        user_inventory = self.inventories[str(user)]
        user_inventory[item["uuid"]] = item
        save_thread = threading.Thread(target=self._save, args=("inventories",))
        save_thread.start()

    def _update_item(self, user, item):
        pass

    def _save(self, files="all"):
        if files in ["saved", "all", "rs"]:
            with open("save.json", 'w') as f_out:
                json.dump(self.saved, f_out)
        if files in ["relationships", "all", "rs"]:
            with open("relationships.json", 'w') as f_out:
                json.dump(self.relationships, f_out)
        if files == "inventories" or files == "all":
            with open("inventories.json", 'w') as f_out:
                json.dump(self.inventories, f_out)

client = KBB()
with open("BOT_KEY.txt", 'r') as f_in:
    bot_key = f_in.read().strip()
client.run(bot_key)
