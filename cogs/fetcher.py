import discord
import aiohttp
import asyncio
import os
from html import unescape
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
IMGS_CHANNEL_ID = int(os.getenv('IMGS_CHANNEL_ID'))

class Fetcher(commands.Cog):

    browser_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML," 
            "like Gecko) Chrome/64.0.3257.0 Safari/537.36"}

    def __init__(self, bot):
        self.bot = bot
        self.get_programming_memes.start()

    def cog_unload(self):
        self.get_programming_memes.cancel()

    @tasks.loop(hours=24.0)
    async def get_programming_memes(self):
        print('Fetching memes...')
        # Using aiohttp module to fetch memes instead of requests module as per the documentation:
        # https://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
        async with aiohttp.ClientSession() as session:
            # I specify the limit of posts here to ensure that we're not bombarding Reddit
            # with requests.
            # If desired, feel free to change the limit. (max is 100)
            # https://www.reddit.com/dev/api/#GET_hot
            LIMIT = 15
            async with session.get(f'https://www.reddit.com/r/ProgrammerHumor/hot.json?limit={LIMIT}', headers=self.browser_headers) as r:
                if r.status == 200:
                    hot = await r.json()
        posts = hot['data']['children']
        memes = [{
            'author': f"reddit - /u/{post['data']['author']}",
            'title': post['data']['title'],
            'url': f"https://www.reddit.com/r{post['data']['permalink']}",
            # Source: https://stackoverflow.com/questions/2087370/decode-html-entities-in-python-string
            'image': unescape(post['data']['preview']['images'][0]['source']['url'])
        } for post in posts if post['data']['link_flair_text'] == 'Meme']
        
        # Get text channel for sending the memes
        guild = discord.utils.get(self.bot.guilds, name=GUILD)
        channel = discord.utils.get(guild.text_channels, id=IMGS_CHANNEL_ID)
        await channel.send('@here **Hello fellow programmers! Here are your latest memes from _r/ProgrammerHumor_ for today!**')

        # Pack each meme into an embed and send it to the specified channel
        for each_meme in memes:
            embed = discord.Embed(color=discord.Color.gold(), 
                description=each_meme['title']
            )
            embed.set_image(url=each_meme['image'])
            embed.set_author(
                name=f"{each_meme['author']}",
                url=each_meme['url']
            )
            await channel.send(embed=embed)
            await asyncio.sleep(1)

        await channel.send('**Want to view more?** https://www.reddit.com/r/ProgrammerHumor/')

    @get_programming_memes.before_loop
    async def before_get_programming_memes(self):
        print('Prepping the bot for fetching the hottest memes of the century...')
        await self.bot.wait_until_ready()
        
def setup(bot):
    bot.add_cog(Fetcher(bot))