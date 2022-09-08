import re
import discord
from discord.ext import commands
from aioconsole import aexec
import sys
import asyncio
import traceback
import os

class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, code: str = ''):
        if 4 >= len(code) >= 2:
            rl = code.rstrip()
        else:
            match = re.search('\n``` *([a-z]{2,4})', code)
            if match:
                rl = match.groups()[0]
                code = code[:-len(rl)]
            else:
                rl = 'py'
            rl = rl.rstrip().lower()
            code.rstrip()
        if not code:
            code = await ctx.message.attachments[0].read()
        else:
            code = code.replace('```py\n', '').replace('\n```', '')
            code.rstrip()
        sys.stdout = open(f'./files/eval-output/eval-{ctx.message.id}.{rl}', 'w', encoding='utf-8')
        sys.stderr = sys.stdout
        failed = False
        try:
            await asyncio.wait_for(aexec(code, {'ctx': ctx, 'self': self, 'code': code}), timeout=5)
        except Exception as exc:
            traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stdout)
            failed = True
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if failed:
            os.rename(f'./files/eval-output/eval-{ctx.message.id}.{rl}', f'./files/eval-output/eval-{ctx.message.id}.py')
            rl = 'py'
        with open(f'./files/eval-output/eval-{ctx.message.id}.{rl}', encoding='utf-8') as fp:
            result = fp.read().replace('\'', '\"').strip().replace('True', 'true').replace('False', 'false').replace('None', 'null')
        if len(result) <= 2000:
            await ctx.reply(
                f'```{rl}\n'
                f'{result}\n'
                f'```',
                allowed_mentions=discord.AllowedMentions(replied_user=False))
        else:
            await ctx.reply(file=discord.File(f'./files/eval-output/eval-{ctx.message.id}.{rl}', f'Result for the command invoked by {ctx.author}.'), allowed_mentions=discord.AllowedMentions(replied_user=False))
        os.remove(f'./files/eval-output/eval-{ctx.message.id}.{rl}')

    @eval.error
    async def eval_error(self, ctx, exc):
        if isinstance(exc, commands.NotOwner):
            await ctx.reply('You are not the Owner of this Bot, so you are not alowed to use this command.',
                            allowed_mentions=discord.AllowedMentions(replied_user=False))

def setup(bot):
    bot.add_cog(DeveloperCommands(bot))