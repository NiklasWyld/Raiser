import discord
import time
import asyncio
from discord.ext import commands

# -------------------------------

class RaiserAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='shutdown')
    async def shutdown(self, ctx: commands.Context):
        await self.bot.close()

    @commands.is_owner()
    @commands.command(name='spam')
    async def spam(self, ctx: commands.Context):
        guild = ctx.guild
        for i in range(100000):
            i = str(i)
            await ctx.guild.create_text_channel(name=f'benedikt-du-bist-ein-kek{i}')
            channel = discord.utils.get(guild.channels, name=f'benedikt-du-bist-ein-kek{i}')
            await channel.send('<@677935302190432287> du kek')

    @commands.is_owner()
    @commands.command(name='send_code_blocks')
    async def send_code_blocks(self, ctx: commands.Context):
        await ctx.send('```')

# -------------------------------

def setup(bot):
    bot.add_cog(RaiserAdmin(bot))