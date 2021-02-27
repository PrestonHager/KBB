# bot_utils.py
# by Preston Hager

import discord

class Message:
    def __init__(self, title, user, content, fields=None, image_path=None):
        self.title = title
        self.user = user
        self.content = content
        self.fields = fields
        self.image_path = image_path

    def create_embed(self):
        embed_title = f"{self.title} | {self.user}" if self.user else self.title
        embed = discord.Embed(
            title=embed_title,
            description=self.content,
            color=0xf013d2,
        )
        if self.fields != None:
            self.fields.create_fields(embed)
        return embed

    async def send(self, channel):
        embed = self.create_embed()
        if self.image_path != None:
            filename = self.image_path.split('/')[-1]
            file = discord.File(self.image_path, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
        else:
            file = None
        await channel.send(embed=embed, file=file)

class MessageFields:
    def __init__(self, *args):
        self.lines = args

    def create_fields(self, embed):
        for line in self.lines:
            embed.add_field(name=line[0], value=line[1], inline=True)
