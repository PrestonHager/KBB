# bot_utils.py
# by Preston Hager

import discord

class Message:
    def __init__(self, title, user, content, task=None, fields=None, image_path=None):
        self.title = title
        self.user = user
        self.content = content
        self.fields = fields
        self.image_path = image_path
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
        embed = self._create_embed()
        file = self._create_image(embed)
        self.sent_message = await channel.send(embed=embed, file=file)
        if self.task != None:
            await self.task.condition.send(self.sent_message)

    async def resend(self):
        if self.sent_message == None:
            raise TypeError("Cannot resend a message that was never sent.")
        else:
            embed = self._create_embed()
            file = self._create_image(embed)
            await self.sent_message.edit(embed=embed)
            if file != None:
                await self.sent_message.channel.send(file=file)

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
    def __init__(self, task_callback, condition, authorized_users, *args, **kwargs):
        self.task_callback = task_callback
        self.condition = condition
        self.authorized_users = authorized_users
        self.args = args
        self.kwargs = kwargs
        self.message = None
        self.complete = False

    async def call(self):
        return await self.task_callback(self.message, *self.args, **self.kwargs)

    async def _finish(self, reaction):
        self.complete = True
        await reaction.clear()

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == self.condition.emoji and user in self.authorized_users and not self.complete:
            if await self.call():
                await self._finish(reaction)
                return True
            else:
                print("Failed on the task callback.")
        return False

class TaskCondition:
    def __init__(self, emoji):
        self.emoji = emoji

    async def send(self, message):
        await message.add_reaction(self.emoji)
