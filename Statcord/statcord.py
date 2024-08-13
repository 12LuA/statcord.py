import discord
import aiohttp
import psutil
from discord import app_commands, Intents, Interaction
from discord.ext import commands, tasks

class StatcordAPI:
    def __init__(self, bot, key: str):
        self.bot = bot
        self.api_url = f"https://statcord.com/api/bots/{bot.user.id}/stats"
        self.headers = {
            "content-type": "application/json",
            "Authorization": key
        }
        self.update_stats.start()

    @tasks.loop(minutes=10)
    async def update_stats(self):
        data = {
            "guildCount": len(self.bot.guilds),
            "shardCount": len(self.bot.shards),
            "userCount": len(self.bot.users),
            "ramUsage": psutil.virtual_memory().used,
            "totalRam": psutil.virtual_memory().total
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=self.headers, json=data) as r:
                print(f"Statcord: {r.status}")
                pass
            await session.close()

    @update_stats.before_loop
    async def before_stats(self): 
        await self.bot.wait_until_ready()

    def stop_auto_post(self):
        self.update_stats.cancel()

class Statcord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statcord_api = StatcordAPI(bot)

    def cog_unload(self):
        self.statcord_api.stop_auto_post()

async def setup(bot):
    await bot.add_cog(Statcord(bot))