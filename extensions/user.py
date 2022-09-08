import discord
import time
import asyncio
import random
from discord.ext import commands
import threading
from discord import ActionRow, Button, ButtonStyle
from translate import Translator, translate

# -------------------------------

class RaiserUser(commands.Cog):
    # __init__
    def __init__(self, bot):
        self.bot = bot
        self.servers = ['A beautiful server', 'A nice server', 'A cool server', 'A great server', 'A wunderfull server']
        self.dice = ['1', '2', '3', '4', '5', '6']
        self.flip = ['Head', 'Number']
        self.no_perms = discord.Embed(title='You do not have all the permissions you need for this command.', colour=discord.Colour.red())
        self.future = discord.Embed(title='This command is not yet available', colour=discord.Colour.random())
        self.helpserver_link = 'https://discord.gg/5erRk6HWrA'
        self.timeout = discord.Embed(title='Timeout', description='You took too long!', colour=discord.Colour.random())
        self.error = discord.Embed(title='Error', description='An error occurred!', colour=discord.Colour.red())

    # Help
    @commands.Cog.slash_command(name='help', description='Displays the Help menu')
    async def _help(self, ctx):
        await ctx.defer()
        embed = (
            discord.Embed(title='Help-Menu', description='Here comes the help menu\n'
                                                         '*All commands are slash commands*\n'
                                                         'Commands marked with (#) are admin commands only.', color=discord.Colour.dark_gold())
                .add_field(name='help', value='Displays the Help menu')
                .add_field(name='server', value='Shows all servers on which the bot is installed')
                .add_field(name='contact', value='Send an invitation to my help server')
                .add_field(name='roll', value='Rolls a cube and shows the number')
                .add_field(name='flip', value='Flips a coin and shows head or number')
                .add_field(name='what_is_better [arg1] [arg2]', value='Randomly picks an argument')
                .add_field(name='clear [limit] (#)', value='Deletes the messages with the limit')
                .add_field(name='ban [member] (#)', value='Bans the specified user')
                .add_field(name='unban [member] (#)', value='Unbans the specified user')
                .add_field(name='kick [member] (#)', value='Kicks the specified user')
                .add_field(name='who_is_better [member1] [member2]', value='Picks randomly a user from this two')
                .add_field(name='send [member] [content]', value='Sends the specified user the specified message')
                .add_field(name='warn [member] [reason] (#)', value='Warns the specified user with the specified reason')
                .add_field(name='ping', value='Pings the bot')
                .add_field(name='time', value='Shows the time')
                .add_field(name='date', value='Shows the date')
                .add_field(name='news [news] [channel] (#)', value='Send a news item to a channel')
                .add_field(name='invite', value='Create an invite link')
                .add_field(name='helpserver', value='Sends a invite to our help server')
                .add_field(name='translate', value='Translate your input')
                .add_field(name='game [game]', value='Does a mini game')
                .add_field(name='userinfo [member]', value='Shows the info for a user')
        )

        await ctx.respond(embed=embed)

    # Server
    @commands.Cog.slash_command(name='server', description='Shows all servers on which the bot is installed')
    async def _server(self, ctx):
        await ctx.defer()
        embed = discord.Embed(title='Server', colour=discord.Colour.dark_purple())
        for server in self.bot.guilds:
            choice = random.choice(self.servers)
            embed.add_field(name=server, value=choice)
        await ctx.respond(embed=embed)

    # Contact
    @commands.Cog.slash_command(name='contact', description='Send an invitation to my help server')
    async def _contact(self, ctx):
        await ctx.defer()
        embed = discord.Embed(title='There is it! Lets go!', description='https://discord.gg/WyzSRETFSW', colour=discord.Colour.dark_blue())
        await ctx.respond(embed=embed)

    # Roll
    @commands.Cog.slash_command(name='roll', description='Rolls a cube and shows the number')
    async def _roll(self, ctx):
        await ctx.defer()
        choice = random.choice(self.dice)
        embed = discord.Embed(title='Here is the result', description=choice, colour=discord.Colour.dark_magenta())
        await ctx.respond(embed=embed)

    # Flip
    @commands.Cog.slash_command(name='flip', description='Flips a coin and shows head or number')
    async def _flip(self, ctx: discord.ApplicationCommandInteraction):
        await ctx.defer()
        choice = random.choice(self.flip)
        embed = discord.Embed(title='Here is the result', description=choice, colour=discord.Colour.dark_red())
        await ctx.respond(embed=embed)

    # what_is_better
    @commands.Cog.slash_command(name='what_is_better', description='Randomly picks an argument')
    async def _what_is_better(self, ctx, arg1, arg2):
        await ctx.defer()
        choice = random.choice([arg1, arg2])
        embed = discord.Embed(title='Here is the result', description=choice, colour=discord.Colour.dark_orange())
        await ctx.respond(embed=embed)

    # Clear
    @commands.Cog.slash_command(name='clear', description='Deletes the messages with the limit')
    async def _clear(self, ctx, limit: int):
        msg = await ctx.defer()
        embed = discord.Embed(title=f'{str(limit)} messages have been deleted by {ctx.author}!', colour=discord.Colour.magenta())
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.respond(embed=self.no_perms, delete_after=10)
        elif ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.channel.purge(limit=int(limit), before=msg)
            await ctx.respond(embed=embed, delete_after=5)

    # Ban
    @commands.Cog.slash_command(name='ban', description='Bans the specified user')
    async def _ban(self, ctx, member: discord.Member, reason='No reason'):
        await ctx.defer()
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.respond(embed=self.no_perms, delete_after=10)
        embed = discord.Embed(title=f'{member.display_name} was banned by {ctx.author}', description=f'Reason: {reason}', colour=discord.Colour.red())
        try:
            await member.send(embed=embed)
        except:
            pass
        await member.ban(reason=reason)
        await ctx.respond(embed=embed, delete_after=10)

    # Unban
    @commands.Cog.slash_command(name='unban', description='Unbans the specified user')
    async def _unban(self, ctx, member: discord.Member, reason='No reason'):
        await ctx.defer()
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.respond(embed=self.no_perms, delete_after=10)
        user = await self.bot.fetch_user(member)
        embed = discord.Embed(title=f'{member} was unbanned by {ctx.author}', description=f'Reason: {reason}', colour=discord.Colour.dark_orange())
        await ctx.guild.unban(user, reason=reason)
        await ctx.respond(embed=embed, delete_after=10)

    # Kick
    @commands.Cog.slash_command(name='kick', description='Kicks the specified user')
    async def _kick(self, ctx, member: discord.Member, reason='No reason'):
        await ctx.defer()
        if not ctx.author.guild_permissions.kick_members:
            return await ctx.respond(embed=self.no_perms)
        embed = discord.Embed(title=f'{member.display_name} was kicked by {ctx.author}', description=f'Reason: {reason}', colour=discord.Colour.dark_red())
        await member.kick(reason=reason)
        try:
            await member.send(embed=embed)
        except:
            pass
        await ctx.respond(embed=embed)

    # Who is better
    @commands.Cog.slash_command(name='who_is_better', description='Picks randomly a user from this two')
    async def _who_is_better(self, ctx, member1: discord.Member, member2: discord.Member):
        await ctx.defer()
        choice = [member1.display_name, member2.display_name]
        result = random.choice(choice)
        embed = discord.Embed(title='Here is the result', description=result, colour=discord.Colour.dark_orange())
        await ctx.respond(embed=embed)

    # Send
    @commands.Cog.slash_command(name='send', description='Sends the specified user the specified message')
    async def _send(self, ctx, member: discord.Member, content):
        await ctx.defer()
        embed = discord.Embed(title=f'Here comes a message from {ctx.author}', description=content, colour=discord.Colour.random())
        try:
            await member.send(embed=embed)
        except:
            return await ctx.respond('This user has deactivated messages from strangers or another error has occurred!', delete_after=10)
        embed2 = discord.Embed(title='Has been sent')
        await ctx.respond(embed=embed2, delete_after=10)

    # Warn
    @commands.Cog.slash_command(name='warn', description='Warns the specified user with the specified reason')
    async def _warn(self, ctx, member: discord.Member, reason='No reason'):
        await ctx.defer()
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond(embed=self.no_perms, delete_after=10)
        embed = discord.Embed(title=f'Attention!', description=f'{member.mention} You have been warned by {ctx.author.mention}!\n'
                                                               f'Reason: {reason}', colour=discord.Colour.red())
        await ctx.respond(embed=embed)
        try:
            await member.send(embed=embed)
        except:
            pass

    # Ping
    @commands.Cog.slash_command(name='ping', description='Pings the bot')
    async def _ping(self, ctx):
        embed = discord.Embed(title=f'{round(self.bot.latency * 1000)}ms', colour=discord.Colour.random())
        await ctx.respond(embed=embed)

    # Time
    @commands.Cog.slash_command(name='time', description='Shows the time')
    async def _time(self, ctx):
        await ctx.defer()
        ttime = time.strftime('%H:%M:%S')
        embed = discord.Embed(title=f'{ttime}', colour=discord.Colour.random())
        await ctx.respond(embed=embed)

    # Date
    @commands.Cog.slash_command(name='date', description='Shows the date')
    async def _date(self, ctx):
        await ctx.defer()
        ddate = time.strftime('%d.%m.%y')
        embed = discord.Embed(title=f'{ddate}', colour=discord.Colour.random())
        await ctx.respond(embed=embed)

    # News
    @commands.Cog.slash_command(name='news', description='Send a news item to a channel')
    async def _news(self, ctx, news, channel: discord.TextChannel):
        await ctx.defer()
        if not type(channel) == discord.TextChannel:
            return await ctx.respond(embed=self.error)
        embed = discord.Embed(title='Attention! News!', description=f'@everyone\n'
                                                                    f'\n'
                                                                    f'**{news}**', colour=discord.Colour.random())
        embed2 = discord.Embed(title='Has been sent')
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=self.no_perms, delete_after=10)
        await channel.send(embed=embed)
        await ctx.respond(embed=embed2, delete_after=5)

    # Invite
    @commands.Cog.slash_command(name='invite', description='Create an invite link')
    async def _invite(self, ctx):
        await ctx.defer()
        link = await ctx.channel.create_invite(max_age=300)
        await ctx.respond(str(link))

    # Help Server
    @commands.Cog.slash_command(name='helpserver', description='Sends a invite to our help server')
    async def _helpserver(self, ctx):
        await ctx.defer()
        embed = discord.Embed(title='Here is your invite!', description=self.helpserver_link, colour=discord.Colour.random())
        await ctx.send(embed=embed)

    # Translate
    @commands.Cog.slash_command(name='translate', description='Translate your input')
    async def _translate(self, ctx, to_lang: str, text: str):
        await ctx.defer()
        if not to_lang:
            return await ctx.respond(embed=self.error)
        if not text:
            return await ctx.respond(embed=self.error)
        translator = Translator(to_lang=to_lang)
        translation = translator.translate(text)
        embed = discord.Embed(title=translation, colour=discord.Colour.dark_blue())
        await ctx.respond(embed=embed)

    # Userinfo
    @commands.Cog.slash_command(name='userinfo', description='Shows the info for a user')
    async def userinfo(self, ctx, member: discord.Member):
        member = member if member else ctx.author
        embed = discord.Embed(title=f'Userinfo for {member.display_name}', colour=discord.Colour.random())
        embed.add_field(name='Server joined', value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"),
                    inline=True)
        embed.add_field(name="Discord joined", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
                    inline=True)
        roles = ''
        for role in member.roles:
            if not role.is_default():
                roles += '{} \r\n'.format(role.mention)
        if roles:
            embed.add_field(name='Roles', value=roles, inline=True)
        embed.set_thumbnail(url=member.display_avatar_url)
        await ctx.respond(embed=embed)

# -------------------------------

# ToDo: Fake Server
# ToDo: HorrorGeschichte

def setup(bot):
    bot.add_cog(RaiserUser(bot))