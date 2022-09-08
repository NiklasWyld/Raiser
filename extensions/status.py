import discord
from discord.ext import commands
import asyncio
import time

# -------------------------------
import main


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='status')
    async def status(self, ctx):
        ttime = time.strftime('%H:%M')
        status = discord.Embed(title='Status', colour=discord.Colour.random(), description=f'Time: {ttime}\n'
                                                                                           f'Bot: {self.bot.user}\n'
                                                                                           f'Owner: niklaspeter123#7578\n'
                                                                                           f'Cogs: {main.cogs}\n'
                                                                                           f'Ping: {round(self.bot.latency * 1000)}ms\n')
        await ctx.send(embed=status)

# -------------------------------

def setup(bot):
    bot.add_cog(Status(bot))
