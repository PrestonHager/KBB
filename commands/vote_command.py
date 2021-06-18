# vote_command.py
# by Preston Hager

import bot_utils as bot

def vote_command(self, message):
    return bot.Message("Vote", message.author, "Vote for KBB on Top.gg!\nhttps://top.gg/bot/812894609289510952/vote")

__all__ = ["vote_command"]
