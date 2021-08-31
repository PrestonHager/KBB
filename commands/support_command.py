# support_command.py
# by Preston Hager

import bot_utils as bot

def support_command(self, message):
    return bot.Message("Support", message.author, "KBB is open source! Support development on Ko-Fi at https://ko-fi.com/prestonhager\n\nIf you need help with a bug or issue, post it on Github at https://github.com/PrestonHager/KBB/issues or DM me on discord (Pi#0005). If you have a feature request for KBB you can also add this to the Github issues page.\n\nThank you for adding KBB to your server, I hope you've had fun with it!")

__all__ = ["support_command"]
