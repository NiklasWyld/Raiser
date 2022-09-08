import time
from discord.ext import commands
import discord
import asyncio
import logging
import pprint
import os

# Logs everything the bot does and what happens in the back-end.
logging.basicConfig(level=logging.INFO)

# -------------------------------

# Main Class of the bot
class Raiser(commands.Bot):
    async def on_ready(self):
        # Sets the activity of the bot to '/help'
        await bot.change_presence(activity=discord.Game('/help'))
        ttime = time.strftime('%H:%M:%S')
        print(f'[*] {self.user} started at {ttime}! And is now ready to start!')

# -------------------------------

# Cogs defined
cogs = ['extensions.admin', 'extensions.user', 'extensions.evalcommand', 'extensions.status', 'extensions.games', 'extensions.support']
bot = Raiser(command_prefix='r.', sync_commands=True)
# Prints all application_commands
pprint.pprint(bot._guild_specific_application_commands)
bot.remove_command('help')

# -------------------------------

for cog in cogs:
    bot.load_extension(cog)

# -------------------------------

bot.run('TOKEN')
