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
    """The main KBB class for the discord bot."""

    # Set up the class variables before anything is called.
    talking_lines = {}
    tasks = {}
    development = False
    data_access_locks = {"user_save": threading.Lock(), "guild_save": threading.Lock()}
    database = DatabaseManager("kbb-users")
    guilds = DatabaseManager("kbb-guilds")
    cached_guilds = {}

    async def on_ready(self):
        # Triggered when the bot sucessfully logs in to discord.
        print("Ready and logged on as {}!\nLoading files....".format(self.user))
        # Load the items for use later.
        with open("items.json", 'r') as f_in:
            items = json.load(f_in)
            self.ALL_ITEMS = items['all']
            self.ALL_RARITY_ITEMS = items['by_rarity']
        # Load each of the texts for the `talk` command.
        texts = [f for f in listdir("texts") if isfile(join("texts", f)) and f.endswith(".txt")]
        for text in texts:
            with open(f"texts/{text}", 'r') as f_in:
                self.talking_lines[text.split(".")[0]] = f_in.read().strip().split('\n')
        # Load the people in for use in the guilds.
        with open("all.csv", 'r') as f_in:
            people = [{"name": l.split(",")[0], "image": l.split(",")[1], "type": l.split(",")[2]} for l in f_in.read().strip().split("\n")[1:]]
        self.guilds.DEFAULT_PEOPLE = people
        print("All files loaded!")

    async def on_message(self, message):
        # Check if development mode is enabled.
        in_dev_channel = message.channel.name in ["kbb-dev", "dev"]
        if self.development == True and not in_dev_channel:
            return False
        elif self.development == False and in_dev_channel:
            return False
        if message.content.startswith(self.command_start(message.guild.id)):
            try:
                # Try to run the command issued.
                await self._command(message)
            except:
                # If it fails, print out the stacktrace without crashing the bot.
                print(f"An exception has occured when {message.author} sent the message \"{message.content}\".")
                traceback.print_exc()

    async def on_reaction_add(self, reaction, user):
        message_id = reaction.message.id
        # Look for the message id in the tasks.
        if message_id in self.tasks.keys():
            # Add the reaction to the task and see if it succeeds.
            succeeded = await self.tasks[message_id].on_reaction_add(reaction, user.id)
            if succeeded:
                del self.tasks[message_id]

    async def _command(self, message):
        # Extract a command from the message and attempt to run it.
        start_time = datetime.datetime.now()
        command = message.content[len(self.command_start(message.guild.id)):].strip().lower().split()
        first_word = command[0]
        if first_word in COMMANDS:
            message_to_send = commands.command(first_word, self, message)
            await self._send_message(message.channel, message_to_send)
        elif first_word == "help":
            await self._send_message(message.channel, bot.Message("Help", False, HELP_MESSAGE))
        else:
            print(f"Received attempted command `{' '.join(command)}` from {message.author.name}.")
            return
        end_time = datetime.datetime.now()
        total_time = end_time - start_time
        # Log the total time to run the command.
        print(f"Received command `{' '.join(command)}` from {message.author.name}. Took {total_time.total_seconds()} seconds to run.")

    async def _send_message(self, channel, message):
        # Send a message in a specific channel and start the task if applicable.
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

    def draw_relationship(self, user_id, guild_id, pool):
        """Draw a relationship from a pool of people."""
        # Aquire any locks needed.
        # TODO: This may be unnecessary.
        self.data_access_locks["user_save"].acquire()
        self.data_access_locks["guild_save"].acquire()
        # Get the user and guild by id
        user = self.database.get_user(int(user_id))
        guild = self.guilds.get_guild(int(guild_id))
        # If the user does not exist or the current relationship does not exist, make a new user.
        if user == None or user['relationships']['current'] == {}:
            user = self.database.new_user(int(user_id))
            user_relationships = user["relationships"]
        # Otherwise, remove the current relationship and add it back to the available pool.
        else:
            user_relationships = user["relationships"]
            person = user_relationships['current']
            user_relationships[person['name']]['married'] = False
            guild["people"].append({"name": person['name'], "image": person['image'], "type": person['type']})
        # Attempt to draw a random person.
        try:
            person = random.choice(pool)
        # TODO: If it fails then handle the error.
        except:
            person = random.choice(self.saved['all'])
        # Set the current relationship and when it was picked.
        user_relationships['current'] = person
        user_relationships['current']['date_picked'] = datetime.datetime.now().isoformat()
        if person['name'] in user_relationships:
            user_relationships[person['name']]['picked'] += 1
        else:
            user_relationships[person['name']] = {"hearts": 0, "total_time": 0, "picked": 1, "married": False, "last_flirt": (datetime.datetime.now() - datetime.timedelta(minutes=2)).isoformat()}
        # Put the user and guild in the database.
        self.database.put_user(int(user_id), user=user)
        # NOTE: we only need to put the people since that was all that was changed.
        self.guilds.put_guild(int(guild_id), people=guild["people"])
        self.data_access_locks["user_save"].release()
        self.data_access_locks["guild_save"].release()
        return person

    def _add_hearts(self, user, amount=1):
        """Add hearts to a user's current relationship by a specific amount."""
        self.data_access_locks["user_save"].acquire()
        # Get the user by id.
        user_relationships = self.database.get_user(int(user.id))["relationships"]
        # Add the hearts to the current relationship.
        person = user_relationships['current']
        user_relationships[person['name']]['hearts'] += amount
        # And put the user in the database.
        # NOTE: we only need to put the relationships since that was all that was changed.
        self.database.put_user(int(user.id), relationships=user_relationships)
        self.data_access_locks["user_save"].release()

    def random_item(self, **kwargs):
        """Draw a random item with weighted rarity.

            common (int)    - the weight of a common item being drawn.
            rare (int)      - the weight of a rare item.
            ultra (int)     - the weight of an ultra item.
        """
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
        """Add an item to a user's inventory."""
        self.data_access_locks["user_save"].acquire()
        # Get the user's inventory.
        user_inventory = self.database.get_user(int(user.id))["inventory"]
        item_found = False
        # Search for the item if stacking is enabled.
        if stack:
            for i in user_inventory:
                item = user_inventory[i]
                if item['item'] == item_name:
                    item['amount'] += amount
                    if item['amount'] <= 0:
                        del item
                    item_found = True
                    break
        # If it was not found or non-stackable, and the amount is at least 1
        # then add it to the inventory as a new item.
        if not item_found and amount > 0:
            item = {
                "uuid": uuid4().hex,
                "name": self._localize(item_name),
                "description": self._localize(item_name, "description"),
                "amount": amount,
                "item": item_name
            }
            user_inventory[item["uuid"]] = item
        # Save the user's inventory and release the lock.
        self.database.put_user(int(user.id), inventory=user_inventory)
        self.data_access_locks["user_save"].release()
        return item

    def command_start(self, guild_id):
        """Get the prefix for a specific guild found by id."""
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
    print("Connecting to discord...")
    client.run(bot_key)
