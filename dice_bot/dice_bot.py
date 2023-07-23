import asyncio
import logging
import random
import discord
from discord.ext import commands

logging.basicConfig(
    filename='logs.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.INFO
)


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='show_help')
    async def print_help(self, ctx):
        await ctx.send('Bot has 2 commands: /dice (for D4, D6, D8, D10, D12, D20, D100) and '
                       '/custom_dice (for any value). To use just call /{command} [number of dice '
                       'sides]')

    @commands.command(name='dice')
    async def throw_dice(self, ctx, dice_type: int, *, is_custom: bool = False):
        if dice_type not in [4, 6, 8, 10, 12, 20, 100] and not is_custom:
            await ctx.send('Wrong dice type! Classic are 4, 6, 8, 10, 12, 20, 100. You can use '
                           '/custom_dice to input any integer value')
            return
        await ctx.send(f'Number on a dice is {random.randint(1, dice_type + 1)}')

    @commands.command(name='custom_dice')
    async def throw_custom_dice(self, ctx, dice_type: int):
        await self.throw_dice(ctx, dice_type, is_custom=True)


class MyBot(commands.Bot):
    async def on_ready(self):
        logging.info(f'Bot {self.user} started')

    async def on_command(self, ctx):
        logging.info(ctx.args)
        logging.info(ctx.command.name + ' success')


TOKEN = ''
intents = discord.Intents.default()
intents.message_content = True
client = MyBot(command_prefix='/', intents=intents)
asyncio.run(client.add_cog(Dice(client)))
client.run(TOKEN)
