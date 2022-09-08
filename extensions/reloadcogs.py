import discord
from discord.ext import commands

# -------------------------------

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cogs = ['extensions.admin', 'extensions.user', 'extensions.evalcommand', 'extensions.status', 'extensions.games', 'extensions.support']

    @commands.is_owner()
    @commands.command(name='reload')
    async def reload(self, ctx: commands.Context, cog: str):
        if not cog:
            for cog1 in self.cogs:
                await self.bot.reload_extension(cog1)
                await ctx.send('All cogs hab been reloaded successfully!')
        if not cog in self.cogs:
            return await ctx.send(f'Attention! {cog} is not available!')
        await self.bot.reload_extension(cog)
        await ctx.send(f'{cog} has been reloaded successfully!')

# -------------------------------

def setup(bot):
    bot.add_cog(Reload(bot))
