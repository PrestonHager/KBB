# main.py
# by Preston Hager

import discord
import bot_utils as bot
import json
import random
import datetime
import threading

HELP_MESSAGE = """**;help** - shows this help message
**;bf** - give me a boyfriend
**;view [person]** - view a current relationship
**;flirt** - flirt with your current relationship for hearts
**;marry [hearts]** - ask your relationship to marry you
**;talk** - talk to your relationship
**;time** - how much time until next day"""

class KBB(discord.Client):
    command_start = ';'
    saved = {"all": [], "available": []}
    relationships = {}
    available_queue = []
    talking_lines = {}

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
        with open("all.csv", 'r') as f_in:
            available = [{"name": l.split(",")[0], "image": l.split(",")[1], "type": l.split(",")[2]} for l in f_in.read().strip().split("\n")[1:]]
        for person in available:
            if person not in self.saved["all"]:
                self.saved["all"].append(person)
                self.saved["available"].append(person)
        with open("texts/dirty.txt", 'r') as f_in:
            self.talking_lines['dirty'] = f_in.read().strip().split('\n')

    async def on_message(self, message):
        if message.content.startswith(self.command_start):
            await self._command(message)

    async def on_reaction_add(self, reaction, user):
        print(reaction)
        print(user)

    async def on_user_update(self, before, after):
        # TODO: add a conversion in database for when user changes
        # their username or discriminator.
        pass

    async def _command(self, message):
        command = message.content[len(self.command_start):].strip().lower()
        command_list = command.split()
        first_word = command_list[0]
        print(f"Received command `{command}` from {message.author.name}")
        if first_word == "time":
            person = self.relationships[str(message.author)]['current']
            last_flirt = datetime.datetime.fromisoformat(self.relationships[str(message.author)][person['name']]['last_flirt'])
            till_next_flirt = datetime.timedelta(seconds=60 * 2 - (datetime.datetime.now() - last_flirt).total_seconds())
            if till_next_flirt < datetime.timedelta(seconds=0):
                flirt_string = "You can flirt with your relationship at any time.\n"
            else:
                hours, remainder = divmod(till_next_flirt.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                formated_time = f"{int(seconds)}s"
                if minutes > 0:
                    formated_time = f"{int(minutes)}m " + formated_time
                if hours > 0:
                    formated_time = f"{int(hours)}h " + formated_time
                flirt_string = f"You can flirt with your relationship in `{formated_time}`\n"
            date_picked = datetime.datetime.fromisoformat(self.relationships[str(message.author)]['current']['date_picked'])
            time_remaining = datetime.timedelta(seconds=24 * 60 * 60 - (datetime.datetime.now() - date_picked).total_seconds())
            if time_remaining < datetime.timedelta(seconds=0):
                await self._send_message(message.channel, bot.Message("Time Left", message.author, f"{flirt_string}You can claim a new relationship at any time."))
                return
            hours, remainder = divmod(time_remaining.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            formated_time = f"{int(seconds)}s"
            if minutes > 0:
                formated_time = f"{int(minutes)}m " + formated_time
            if hours > 0:
                formated_time = f"{int(hours)}h " + formated_time
            await self._send_message(message.channel, bot.Message("Time Left", message.author, f"{flirt_string}You have `{formated_time}` until you can claim a new relationship."))
        elif first_word == "bf":
            if len(self.saved['available']) == 0:
                await self._send_message(message.channel, bot.Message("Boyfriend", message.author, "I'm out of boyfriends!"))
            elif str(message.author) in self.relationships:
                date_picked = datetime.datetime.fromisoformat(self.relationships[str(message.author)]['current']['date_picked'])
                if (datetime.datetime.now() - date_picked).total_seconds() < 24 * 60 * 60:
                    await self._send_message(message.channel, bot.Message("Boyfriend", message.author, "You already have a boyfriend, you can't have another right now."))
                    return
            boyfriend = self._draw_boyfriend(message.author)
            await self._send_message(message.channel, bot.Message("Boyfriend", message.author, f"You have **{boyfriend['name']}**!\nEnjoy your time together!"), f"images/{boyfriend['image']}")
        elif first_word == "view":
            if len(command_list) > 1:
                if len(message.mentions) < 1:
                    await self._send_message(message.channel, bot.Message("View Relationship", message.author, "You must supply either a mention or nothing (for yourself)"))
                    return
                user = str(message.mentions[0])
                print(user)
            else:
                user = message.author
            if str(user) in self.relationships and 'current' in self.relationships[str(user)]:
                person = self.relationships[str(user)]['current']
                s = 'You are' if user == message.author else message.mentions[0].mention + ' is'
                hearts = self.relationships[str(user)][person['name']]['hearts']
                married = "Yes" if self.relationships[str(user)][person['name']]['married'] else "No"
                await self._send_message(message.channel, bot.Message("View Relationship", message.author, f"{s} with **{person['name']}** right now.", bot.MessageFields(("❤️", f"+**{hearts}**"), ("💍", f"{married}"))), f"images/{person['image']}")
            else:
                s = 'You don\'t' if user == message.author else message.mentions[0].mention + ' doesn\'t'
                await self._send_message(message.channel, bot.Message("View Relationship", message.author, f"{s} have a relationship yet."))
        elif first_word == "flirt":
            if str(message.author) in self.relationships and 'current' in self.relationships[str(message.author)]:
                person = self.relationships[str(message.author)]['current']
                last_flirt = datetime.datetime.fromisoformat(self.relationships[str(message.author)][person['name']]['last_flirt'])
                if (datetime.datetime.now() - last_flirt).total_seconds() < 60 * 2:
                    await self._send_message(message.channel, bot.Message("Flirt", message.author, "You must wait at least 2 minutes between flirts."))
                    return
                self.relationships[str(message.author)][person['name']]['last_flirt'] = datetime.datetime.now().isoformat()
                hearts = int(random.random() * 3)
                if hearts < 1:
                    await self._send_message(message.channel, bot.Message("Flirt", message.author, "You didn't gain any ❤️. Better luck next time."))
                else:
                    person = self.relationships[str(message.author)]['current']
                    self._add_hearts(message.author, hearts)
                    await self._send_message(message.channel, bot.Message("Flirt", message.author, f"You gained {hearts} ❤️ with {person['name']}!"))
            else:
                await self._send_message(message.channel, bot.Message("Flirt", message.author, "You must be in a relationship to do this."))
        elif first_word == "marry":
            if str(message.author) in self.relationships and 'current' in self.relationships[str(message.author)]:
                user_relationships = self.relationships[str(message.author)]
                person = user_relationships['current']
                hearts = user_relationships[person['name']]['hearts']
                if hearts >= 25:
                    if len(command_list) > 1:
                        try:
                            tried_hearts = int(command_list[1])
                            if tried_hearts > hearts:
                                await self._send_message(message.channel, bot.Message("Marry", message.author, "You cannot use ❤️ that you don't have!"))
                            else:
                                percentage = hearts * 3 / 100
                                chance = random.random()
                                user_relationships[person['name']]['hearts'] -= tried_hearts
                                if chance <= percentage:
                                    user_relationships[person['name']]['married'] = True
                                    await self._send_message(message.channel, bot.Message("Marry", message.author, f"You are now married to {person['name']}!"))
                                else:
                                    await self._send_message(message.channel, bot.Message("Marry", message.author, f"{person['name']} rejected you, better luck next time."))
                            return
                        except ValueError:
                            pass
                    await self._send_message(message.channel, bot.Message("Marry", message.author, "Include how many ❤️ you want to put towards the marriage.\n1 ❤️ is +3\% chance. Minimum of 25 ❤️."))
                else:
                    await self._send_message(message.channel, bot.Message("Marry", message.author, f"You don't have enough ❤️ to ask {person['name']} to marry you."))
            else:
                await self._send_message(message.channel, bot.Message("Marry", message.author, "You must be in a relationship to do this."))
        elif first_word == "talk":
            if str(message.author) in self.relationships and 'current' in self.relationships[str(message.author)]:
                person = self.relationships[str(message.author)]['current']
                line = random.choice(self.talking_lines['dirty'])
                await self._send_message(message.channel, bot.Message("Talk", message.author, f"{person['name']} says \"{line}\""))
            else:
                await self._send_message(message.channel, bot.Message("Talk", message.author, "You must be in a relationship to do this."))
        elif first_word == "help":
            await self._send_message(message.channel, bot.Message("Help", False, HELP_MESSAGE))

    async def _send_message(self, channel, message, image_path=None):
        embed = message.create_embed()
        if image_path != None:
            filename = image_path.split('/')[-1]
            file = discord.File(image_path, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
        else:
            file = None
        await channel.send(embed=embed, file=file)

    def _draw_boyfriend(self, user):
        if str(user) not in self.relationships:
            self.relationships[str(user)] = {}
        else:
            person = self.relationships[str(user)]['current']
            del person['date_picked']
            self.relationships[str(user)][person['name']]['married'] = False
            self.available_queue.append(person)
        user_relationships = self.relationships[str(user)]
        person = random.choice(self.saved['available'])
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
        save_thread = threading.Thread(target=self._save)
        save_thread.start()
        return person

    def _add_hearts(self, user, amount=1):
        user_relationships = self.relationships[str(user)]
        person = user_relationships['current']
        user_relationships[person['name']]['hearts'] += amount
        save_thread = threading.Thread(target=self._save)
        save_thread.start()

    def _save(self):
        with open("save.json", 'w') as f_out:
            json.dump(self.saved, f_out)
        with open("relationships.json", 'w') as f_out:
            json.dump(self.relationships, f_out)

client = KBB()
with open("BOT_KEY.txt", 'r') as f_in:
    bot_key = f_in.read().strip()
client.run(bot_key)
