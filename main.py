import discord
from discord.ext import commands
import cogs

import yaml

import cogs.voice_kick_roulette

INTENTS = discord.Intents.all()

bot = commands.Bot(command_prefix="daun", intents=INTENTS)


def get_config():
    with open("config.yml", "r", encoding="UTF-8") as f:
        return yaml.safe_load(f)


config = get_config()

bot = commands.Bot(command_prefix=config["prefix"], intents=INTENTS)


@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}, prefix: {config['prefix']}")
    await bot.change_presence(status=discord.Status.invisible)
    
    print("Loading cogs...")

    bot.add_cog(cogs.AutoAnswers(bot, config["phrases"]))
    bot.add_cog(cogs.AutoVoice(bot))
    bot.add_cog(cogs.VoiceKickRoulette(bot))

    print("Cogs loaded.")

    # await bot.change_presence(activity=discord.Game(name="с твоей писей"))

    print("Bot is ready to go.")


bot.run(config["token"])
