# bot_utils.py
# by Preston Hager

import asyncio
import discord
import threading

class Message:
    def __init__(self, title, user, content, task=None, fields=None, image_path=None, footer=discord.Embed.Empty, footer_icon=discord.Embed.Empty):
        self.title = title
        self.user = user
        self.content = content
        self.fields = fields
        self.image_path = image_path
        self.footer_text = footer
        self.footer_icon = footer_icon
        self.task = task
        if task != None:
            self.task.message = self

    def create_task(self):
        return self.task

    def _create_embed(self):
        embed_title = f"{self.title} | {self.user}" if self.user else self.title
        embed = discord.Embed(
            title=embed_title,
            description=self.content,
            color=0xf013d2,
        )
        embed.set_footer(text=self.footer_text, icon_url=self.footer_icon)
        if self.fields != None:
            self.fields.create_fields(embed)
        return embed

    def _create_image(self, embed):
        if self.image_path != None:
            filename = self.image_path.split('/')[-1]
            file = discord.File(self.image_path, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
        else:
            file = None
        return file

    async def send(self, channel):
        self.embed = self._create_embed()
        self.file = self._create_image(self.embed)
        self.sent_message = await channel.send(embed=self.embed, file=self.file)
        if self.task != None:
            for condition in self.task.conditions:
                await condition.send(self.sent_message)
            if self.task.expires > 0:
                self.task_expire_thread = threading.Timer(float(self.task.expires), asyncio.run_coroutine_threadsafe, args=(self._expire_task(), asyncio.get_running_loop()))
                self.task_expire_thread.start()

    async def resend(self):
        if self.sent_message == None:
            raise TypeError("Cannot resend a message that was never sent.")
        else:
            self.embed = self._create_embed()
            self.file = self._create_image(self.embed)
            await self.sent_message.edit(embed=self.embed)
            if self.file != None:
                await self.sent_message.channel.send(file=self.file)

    async def _expire_task(self):
        self.task_expire_thread = None
        await self.task._finish()
        # self.embed.set_footer(text="*This message has expired.*")
        self.footer_text = "🕒 This message has expired."
        await self.resend()

    def edit(self, title=None, user=None, content=None, fields=None, image_path=None):
        if title != None:
            self.title = title
        if user != None:
            self.user = user
        if content != None:
            self.content = content
        if fields != None:
            self.fields = fields
        if image_path != None:
            self.image_path = image_path

class MessageFields:
    def __init__(self, *args):
        self.lines = args

    def create_fields(self, embed):
        for line in self.lines:
            embed.add_field(name=line[0], value=line[1], inline=True)

class Task:
    def __init__(self, conditions, users_list, whitelist=True, expires=-1):
        self.conditions = conditions
        self.users_list = users_list
        self.whitelist = whitelist
        self.expires = expires
        self.message = None
        self.complete = False
        self.users_reacted = []

    async def _finish(self):
        self.complete = True
        for condition in self.conditions:
            await self.message.sent_message.clear_reaction(condition.emoji)
        if self.message.task_expire_thread != None:
            self.message.task_expire_thread.cancel()

    async def on_reaction_add(self, reaction, user):
        if ((self.whitelist and user in self.users_list) or (not self.whitelist and user not in self.users_list)) and not self.complete and user not in self.users_reacted:
            for condition in self.conditions:
                if reaction.emoji == condition.emoji:
                    self.users_reacted.append(user)
                    if await condition.call(self.message):
                        await self._finish()
                        return True
                    else:
                        return False
        return False

class TaskCondition:
    def __init__(self, emoji, callback, *args, **kwargs):
        self.emoji = emoji
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    async def call(self, message):
        return await self.callback(message, *self.args, **self.kwargs)

    async def send(self, message):
        await message.add_reaction(self.emoji)
