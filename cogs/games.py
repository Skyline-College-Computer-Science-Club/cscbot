import random
import discord
from discord.ext import commands

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Rolls the dice, ranging from either 1 to 100.")
    async def rtd(self, ctx):
        """ Rolls the dice and randomly generates a number. """
        number = random.randint(0, 100)
        message = f'{ctx.author.mention} rolled: `{str(number)}`'
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Games(bot))