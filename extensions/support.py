import discord
from discord import ActionRow, Button, ButtonStyle
import asyncio
import time
import random
from discord.ext import commands
from datetime import datetime

# -------------------------------

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Cooldown
    @commands.Cog.slash_command(name='support', description='Get support from a supporter')
    async def support(self, ctx, reason: str):
        await ctx.defer()

        now = datetime.now()
        today = datetime.today()

        components = [ActionRow(
            Button(label='Support', custom_id='support_support', style=ButtonStyle.red),
            Button(label='Bot-Support', custom_id='support_bot_support', style=ButtonStyle.green)
        )]

        embed = discord.Embed(title='What kind of support do you need?', colour=discord.Colour.random())
        msg = await ctx.respond(embed=embed, components=components, delete_after=10)

        def _check(i: discord.ComponentInteraction, b):
            return i.message == msg and i.member == ctx.author

        interaction, button = await self.bot.wait_for('button_click', check=_check)
        button_id = button.custom_id

        await interaction.defer()

        embed1 = discord.Embed(title='Your request is now being processed. Please wait a moment. ⌛',
                               colour=discord.Colour.random())
        await ctx.respond(embed=embed1, delete_after=10)

        if button_id == 'support_support':
            await self.support_support(ctx, interaction, components, now, today, reason)

        elif button_id == 'support_bot_support':
            await self.bot_support(ctx, interaction, components, now, today, reason)

    async def bot_support(self, ctx: commands.Context, interaction, components: list, now, today, reason):
        await interaction.respond('This command is still under development.',
                          delete_after=5)

    async def support_support(self, ctx: commands.Context, interaction, components: list, now, today, reason):
        await interaction.edit(components=components[0].disable_all_buttons())

        if discord.utils.get(ctx.guild.categories, name='Support'):
            category = discord.utils.get(ctx.guild.categories, name='Support')
        else:
            category = await ctx.guild.create_category(name='Support')

        channel = await category.create_text_channel(name='Support-' + str(ctx.author.id))
        await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await channel.set_permissions(ctx.author, view_channel=True)

        self.components_2 = [
            ActionRow(
                Button(label='Close ticket', style=ButtonStyle.red, custom_id='close_support')
            )
        ]

        embed2 = discord.Embed(
            title=f'{ctx.author.name} | Support | {now.strftime("%H:%M:%S")} | {today.strftime("%d.%m.%Y")}',
            description=f'Reason: {reason}', colour=discord.Colour.random())
        embed2.set_footer(text=f'A supporter will soon take care of you {ctx.author.name}!')
        await channel.send(embed=embed2, components=self.components_2)

    @commands.Cog.on_click(custom_id='close_support')
    async def on_click_close_support(self, interaction: discord.ComponentInteraction, button):
        now = datetime.now()
        today = datetime.today()

        embed = discord.Embed(title='Support ticket is closed 🔒', description=f'Ticket closed at {now.strftime("%H:%M:%S")}')
        await interaction.respond(embed=embed)
        await interaction.edit(components=[ActionRow(button)][0].disable_all_components())

        channel_name = interaction.channel.name
        user_id = channel_name.split('-')[1]
        member = await self.bot.fetch_user(int(user_id))

        await interaction.channel.set_permissions(member, send_messages=False)

# -------------------------------

def setup(bot):
    bot.add_cog(Support(bot))