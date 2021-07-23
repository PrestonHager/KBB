# main.py
# by Preston Hager

import discord
import json
import random
import datetime
import threading
import traceback
from os import listdir
from os.path import isfile, join, split
from uuid import uuid4

import commands
import bot_utils as bot
from database_manager import *

HELP_MESSAGE = """**;help** - shows this help message
**;bf** - give me a boyfriend
**;gf** - give me a girlfriend
**;view [person]** - view a current relationship
**;flirt** - flirt with your current relationship for hearts
**;marry [hearts]** - ask your relationship to marry you
**;talk** - talk to your relationship
**;time** - how much time until next day
**;pickup [line]** - try to gain hearts based on a pickup line you write
**;items** - view the items in your inventory
**;open** - open a mystery box if you have one
**;vote** - vote for KBB and earn rewards!"""
COMMANDS = ["time", "bf", "gf", "xf", "view", "flirt", "marry", "talk", "pickup", "vote", "items", "open", "prefix"]

class KBB(discord.Client):
    saved = {"all": [], "available": []}
    available_queue = []
    talking_lines = {}
    tasks = {}
    development = False
    data_access_locks = {"save": threading.Lock(), "rel": threading.Lock(), "inv": threading.Lock()}
    database = DatabaseManager("kbb-users")
    guilds = DatabaseManager("kbb-guilds")
    cached_guilds = {}

    async def on_ready(self):
        print("Ready and logged on as {}!\nLoading files....".format(self.user))
        with open("items.json", 'r') as f_in:
            items = json.load(f_in)
            self.ALL_ITEMS = items['all']
            self.ALL_RARITY_ITEMS = items['by_rarity']
        try:
            with open("save.json", 'r') as f_in:
                self.saved = json.load(f_in)
        except:
            self.saved = {"all": [], "available": []}
        texts = [f for f in listdir("texts") if isfile(join("texts", f)) and f.endswith(".txt")]
        for text in texts:
            with open(f"texts/{text}", 'r') as f_in:
                self.talking_lines[text.split(".")[0]] = f_in.read().strip().split('\n')
        with open("all.csv", 'r') as f_in:
            available = [{"name": l.split(",")[0], "image": l.split(",")[1], "type": l.split(",")[2]} for l in f_in.read().strip().split("\n")[1:]]
        for person in available:
            if person not in self.saved["all"]:
                self.saved["all"].append(person)
                self.saved["available"].append(person)
        save_thread = threading.Thread(target=self._save, args=("saved",))
        save_thread.start()
        print("All files loaded!")

    async def on_message(self, message):
        in_dev_channel = message.channel.name in ["kbb-dev", "dev"]
        if self.development == True and not in_dev_channel:
            return False
        elif self.development == False and in_dev_channel:
            return False
        if message.content.startswith(self.command_start(message.guild.id)):
            try:
                await self._command(message)
            except:
                print(f"An exception has occured when {message.author.id} send the message `{message}`.")
                traceback.print_exc()

    async def on_reaction_add(self, reaction, user):
        message_id = reaction.message.id
        if message_id in self.tasks.keys():
            succeeded = await self.tasks[message_id].on_reaction_add(reaction, user.id)
            if succeeded:
                del self.tasks[message_id]

    async def _command(self, message):
        command = message.content[len(self.command_start(message.guild.id)):].strip().lower().split()
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
        return self._draw_relationship_from_pool(user.id, pool)

    def draw_girlfriend(self, user):
        pool = [d for d in self.saved['available'] if d['type'] == 'gf']
        return self._draw_relationship_from_pool(user.id, pool)

    def draw_relationship(self, user):
        pool = self.saved['available']
        return self._draw_relationship_from_pool(user.id, pool)

    def _draw_relationship_from_pool(self, user_id, pool):
        self.data_access_locks["rel"].acquire()
        self.data_access_locks["save"].acquire()
        user = self.database.get_user(int(user_id))
        if user == None or user['relationships']['current'] == {}:
            user = self.database.new_user(int(user_id))
            user_relationships = user["relationships"]
        else:
            user_relationships = user["relationships"]
            person = user_relationships['current']
            del person['date_picked']
            if person != {}:
                user_relationships[person['name']]['married'] = False
                self.available_queue.append(person)
        try:
            person = random.choice(pool)
        except:
            person = random.choice(self.saved['all'])
        user_relationships['current'] = person
        user_relationships['current']['date_picked'] = datetime.datetime.now().isoformat()
        if person['name'] in user_relationships:
            user_relationships[person['name']]['picked'] += 1
        else:
            user_relationships[person['name']] = {"hearts": 0, "total_time": 0, "picked": 1, "married": False, "last_flirt": (datetime.datetime.now() - datetime.timedelta(minutes=2)).isoformat()}
        self.saved['available'].remove(person)
        if len(self.available_queue) > 0:
            self.saved['available'].append(self.available_queue[-1])
            self.available_queue.pop()
        self.database.put_user(int(user_id), user=user)
        self.data_access_locks["rel"].release()
        self.data_access_locks["save"].release()
        save_thread = threading.Thread(target=self._save, args=("saved",))
        save_thread.start()
        return person

    def _add_hearts(self, user, amount=1):
        self.data_access_locks["rel"].acquire()
        user_relationships = self.database.get_user(int(user.id))["relationships"]
        person = user_relationships['current']
        user_relationships[person['name']]['hearts'] += amount
        self.database.put_user(int(user.id), relationships=user_relationships)
        self.data_access_locks["rel"].release()

    def random_item(self, **kwargs):
        def weighted_random(weights):
            total = sum(i for i in weights.values())
            r = random.randint(1, total)
            for value in weights:
                r -= weights[value]
                if r <= 0: return value
        weights = {
            "common": 0,
            "rare": 0,
            "ultra": 0
        }
        weights.update(kwargs)
        item_rarity = weighted_random(weights)
        return random.choice(self.ALL_RARITY_ITEMS[item_rarity])

    def _add_item(self, user, item_name, stack=True, amount=1):
        self.data_access_locks["inv"].acquire()
        user_inventory = self.database.get_user(int(user.id))["inventory"]
        item_found = False
        if stack:
            for i in user_inventory:
                item = user_inventory[i]
                if item['item'] == item_name:
                    item['amount'] += amount
                    if item['amount'] <= 0:
                        del item
                    item_found = True
                    break
        if not item_found and amount > 0:
            item = {
                "uuid": uuid4().hex,
                "name": self._localize(item_name),
                "description": self._localize(item_name, "description"),
                "amount": amount,
                "item": item_name
            }
            user_inventory[item["uuid"]] = item
        self.database.put_user(int(user.id), inventory=user_inventory)
        self.data_access_locks["inv"].release()
        return item

    def command_start(self, guild_id):
        if guild_id in self.cached_guilds:
            return self.cached_guilds[guild_id]["prefix"]
        else:
            guild = self.guilds.get_guild(guild_id)
            if guild == None:
                guild = self.guilds.new_guild(guild_id)
            self.cached_guilds[guild_id] = guild
            return guild["prefix"]

    def _localize(self, item, loc_type="name"):
        if loc_type == "name":
            return self.ALL_ITEMS[item]['name']
        elif loc_type == "description":
            return self.ALL_ITEMS[item]['description']

    def _save(self, files="saved"):
        with open("save.json", 'w') as f_out:
            json.dump(self.saved, f_out)

if __name__ == "__main__":
    import sys
    intents = discord.Intents.default()
    intents.members = True
    client = KBB(intents=intents)
    if len(sys.argv) > 1:
        options = [i.lower() for i in sys.argv[1:]]
        if "-d" in options or "--dev" in options:
            print("Starting in development mode.")
            client.development = True
    with open("BOT_KEY.txt", 'r') as f_in:
        bot_key = f_in.read().strip()
    client.run(bot_key)
