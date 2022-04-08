import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Intialize bot and all of the intents
# discord.Intents.all() basically gives the bot superpowers
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
# Source: https://stackoverflow.com/questions/65203363/how-to-load-multiple-cogs-in-python-3
if __name__ == '__main__':
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != '__init__.py':
            bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print("BOT IS NOW TURNING ON GUYS!!!!!!")
    print(f"Joining {GUILD}...")
    await bot.change_presence(activity=discord.Game(name="Doing STEM Center things... || !help"))  

@bot.event
async def on_member_join(member):
    # May need to adjust the channel location for the comp sci club
    channel = member.guild.text_channels[0]
    await channel.send(f'Welcome to the the greatest club in Skyline College history {member.mention}! :D')

@bot.event
async def on_message(message):
    """ Responds if b00chan types. """
    boochan_id = 316816595668172800
    emoji = '👍'
    if message.author.id == boochan_id:
        bot_msg = f"<@{message.author.id}> ||L+ratio||"
        bot_msg = await message.channel.send(bot_msg)
        await bot_msg.add_reaction(emoji)
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    """ Error handling for bot commands """
    
    if isinstance(error, commands.MissingPermissions):
        message = 'Sorry, you don\'t have access to this command.'
        
    elif isinstance(error, commands.CommandOnCooldown):
        message = f'Stop spamming the commands!!!!! Please wait {error.retry_after:.1f} seconds.'

    elif isinstance(error, commands.MissingRequiredArgument):
        message = 'You\'re missing an argument in that command. Use !help if you need to.'

    elif isinstance(error, TimeoutError):
        message = "Oops! Timeout error!"

    elif isinstance(error, commands.TooManyArguments):
        message = 'You added too many arguments in that command. Use !help if you need to.'
    
    elif isinstance(error, commands.BotMissingPermissions):
        message = 'Hmm, it seems like I need permission to perform that command. Complain to the officers for me!'

    elif isinstance(error, commands.NotOwner):
        message = 'You have to be the owner of this bot, aka me, to perform this command!'

    else:
        message = error

    # Keep chat logs clean
    await ctx.send(message, delete_after=10)
    await ctx.message.delete(delay=10)

# Execute client
bot.run(TOKEN, bot=True, reconnect=True)

