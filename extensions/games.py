import discord
from discord import ActionRow, Button, ButtonStyle
import asyncio
import time
import random
from discord.ext import commands

# -------------------------------

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ssp = ['ssp_scissors', 'ssp_stone', 'ssp_paper']

    @commands.Cog.slash_command(name='game', description='Does a mini game', options=[discord.SlashCommandOption(
        option_type=str, name='game', description='Choice a game to play', choices=[
            discord.SlashCommandOptionChoice(name='Numberquiz', value='numberquiz'),
            discord.SlashCommandOptionChoice(name='ScissorsStonePaper', value='scissorsstonepaper')
        ]
    )])
    async def game(self, ctx, game: str):
        if game == 'numberquiz':
            await self.numberquiz(ctx=ctx)
        elif game == 'scissorsstonepaper':
            await self.scissorsstonepaper(ctx=ctx)

    # -------------------------------

    async def numberquiz(self, ctx):
        components = [
            ActionRow(
                Button(label='️1', custom_id='numberquiz_1', style=ButtonStyle.green),
                Button(label='️2', custom_id='numberquiz_2', style=ButtonStyle.Secondary),
                Button(label='3', custom_id='numberquiz_3', style=ButtonStyle.red)
            )
        ]

        embed = discord.Embed(title='Choice an number', colour=discord.Colour.random())
        msg = await ctx.respond(embed=embed, components=components)

    # -------------------------------

    async def scissorsstonepaper(self, ctx):
        components = [
            ActionRow(
                Button(label='️Scissors', custom_id='ssp_scissors', style=ButtonStyle.green),
                Button(label='Stone', custom_id='ssp_stone', style=ButtonStyle.Secondary),
                Button(label='Paper', custom_id='ssp_paper', style=ButtonStyle.red)
            )
        ]

        embed = discord.Embed(title='Choice an option', colour=discord.Colour.random())
        msg = await ctx.respond(embed=embed, components=components)

    # -------------------------------

    # -------------- On Click Numberquiz -----------------

    @commands.Cog.on_click(custom_id='numberquiz_1')
    async def numberquiz_1(self, interaction, button):
        iinteger = random.randint(1, 3)
        integer = 'numberquiz_' + str(iinteger)
        iinteger = str(iinteger)
        if str(button.custom_id) == str(integer):
            await interaction.respond(f'**Right!** The number was {iinteger}', delete_after=5)
        else:
            await interaction.respond(f'**Try again!** The number was {iinteger}', delete_after=5)

    @commands.Cog.on_click(custom_id='numberquiz_2')
    async def numberquiz_2(self, interaction, button):
        iinteger = random.randint(1, 3)
        integer = 'numberquiz_' + str(iinteger)
        iinteger = str(iinteger)
        if str(button.custom_id) == str(integer):
            await interaction.respond(f'**Right!** The number was {iinteger}', delete_after=5)
        else:
            await interaction.respond(f'**Try again!** The number was {iinteger}', delete_after=5)

    @commands.Cog.on_click(custom_id='numberquiz_3')
    async def numberquiz_3(self, interaction, button):
        iinteger = random.randint(1, 3)
        integer = 'numberquiz_' + str(iinteger)
        iinteger = str(iinteger)
        if str(button.custom_id) == str(integer):
            await interaction.respond(f'**Right!** The number was {iinteger}', delete_after=5)
        else:
            await interaction.respond(f'**Try again!** The number was {iinteger}', delete_after=5)

    # -------------- On Click Numberquiz -----------------

    # -------------- On Click SSP -----------------

    @commands.Cog.on_click(custom_id='ssp_scissors')
    async def ssp_scissors(self, interaction, button):
        u = button.custom_id
        choice = random.choice(self.ssp)
        if choice == self.ssp[0]:
            new_choice = "Scissors"
        elif choice == self.ssp[1]:
            new_choice = "Stone"
        elif choice == self.ssp[2]:
            new_choice = "Paper"
        if choice == button.custom_id:
            await interaction.respond(f'**Tie** U: {button.label} C: {new_choice}', delete_after=5)
        elif (u == self.ssp[0] and choice == self.ssp[2]) or (u == self.ssp[1] and choice == self.ssp[0]) or (u == self.ssp[2] and choice == self.ssp[1]):
            await interaction.respond(f'**You Win** U: {button.label} C: {new_choice}', delete_after=5)
        elif (u == self.ssp[0] and choice == self.ssp[1]) or (u == self.ssp[1] and choice == self.ssp[2]) or (u == self.ssp[2] and choice == self.ssp[0]):
            await interaction.respond(f'**You Lose** U: {button.label} C: {new_choice}', delete_after=5)

    @commands.Cog.on_click(custom_id='ssp_stone')
    async def ssp_stone(self, interaction, button):
        u = button.custom_id
        choice = random.choice(self.ssp)
        if choice == self.ssp[0]:
            new_choice = "Scissors"
        elif choice == self.ssp[1]:
            new_choice = "Stone"
        elif choice == self.ssp[2]:
            new_choice = "Paper"
        if choice == button.custom_id:
            await interaction.respond(f'**Tie** U: {button.label} C: {new_choice}', delete_after=5)
        elif (u == self.ssp[0] and choice == self.ssp[2]) or (u == self.ssp[1] and choice == self.ssp[0]) or (
                u == self.ssp[2] and choice == self.ssp[1]):
            await interaction.respond(f'**You Win** U: {button.label} C: {new_choice}', delete_after=5)
        elif (u == self.ssp[0] and choice == self.ssp[1]) or (u == self.ssp[1] and choice == self.ssp[2]) or (
                u == self.ssp[2] and choice == self.ssp[0]):
            await interaction.respond(f'**You Lose** U: {button.label} C: {new_choice}', delete_after=5)

    @commands.Cog.on_click(custom_id='ssp_paper')
    async def ssp_paper(self, interaction, button):
        u = button.custom_id
        choice = random.choice(self.ssp)
        if choice == self.ssp[0]:
            new_choice = "Scissors"
        elif choice == self.ssp[1]:
            new_choice = "Stone"
        elif choice == self.ssp[2]:
            new_choice = "Paper"
        if choice == button.custom_id:
            await interaction.respond(f'**Tie** U: {button.label} C: {new_choice}', delete_after=5)
        elif (u == self.ssp[0] and choice == self.ssp[2]) or (u == self.ssp[1] and choice == self.ssp[0]) or (
                u == self.ssp[2] and choice == self.ssp[1]):
            await interaction.respond(f'**You Win** U: {button.label} C: {new_choice}', delete_after=5)
        elif (u == self.ssp[0] and choice == self.ssp[1]) or (u == self.ssp[1] and choice == self.ssp[2]) or (
                u == self.ssp[2] and choice == self.ssp[0]):
            await interaction.respond(f'**You Lose** U: {button.label} C: {new_choice}', delete_after=5)

    # -------------- On Click SSP -----------------

# -------------------------------

def setup(bot):
    bot.add_cog(Games(bot))