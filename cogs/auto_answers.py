import discord.ext.commands as commands
import random
import logging as log

class AutoAnswers(commands.Cog):
    def __init__(self, bot, phrases: list[str]):
        self.bot = bot
        self.phrases = phrases

    @commands.Cog.listener()
    async def on_message(self, message):
        # if bot is mentioned, reply with a message
        if (self.bot.user.mentioned_in(message) or random.random() < 0.2) and not message.author.bot:
            await message.reply(random.choice(self.phrases))
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Auto Answers cog loaded.")