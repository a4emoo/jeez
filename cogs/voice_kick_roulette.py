import discord.ext.commands as commands
from discord.ext.commands import Cog
import os.path as path
import os
import asyncio
import random
import discord

class VoiceKickRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_kick = None
        self.sounds = os.listdir(path.join(os.getcwd(), "sounds", "voice_kick_roulette"))

    # @commands.is_owner()
    @commands.command(name="ls")
    async def list_sounds(self, ctx: commands.Context):
        """List all sounds available for the voice kick roulette."""
        sounds = (
            ", ".join(self.sounds) if self.sounds else "хихихи хохохо нищий без звуков"
        )
        await ctx.reply(sounds)

    async def play_random_sound(self, vc: discord.VoiceClient, n: int = 1, prefix_include: str = None, prefix_exclude: str = None):
        sounds = [s for s in self.sounds if s.startswith(prefix_include)] if prefix_include else self.sounds        
        sounds = [s for s in sounds if not s.startswith(prefix_exclude)] if prefix_exclude else sounds
        for _ in range(n):
            choise = random.choice(sounds)
            sounds.remove(choise)
            await vc.play(
                discord.FFmpegPCMAudio(
                    path.join(
                        os.getcwd(),
                        "sounds",
                        "voice_kick_roulette",
                        choise,
                    )
                ),
                wait_finish=True,
            )

    @commands.command(name="debosh")
    async def roulette(self, ctx: commands.Context):
        """Play a random sound from the voice kick roulette."""
        if not self.sounds:
            await ctx.reply("хихихи хохохо нищий без звуков")
            return

        await ctx.author.voice.channel.connect()
        voice_client = ctx.voice_client
        try:
            await self.play_random_sound(voice_client, 2, prefix_exclude="countdown")
        except Exception as e:
            await ctx.reply(f"поссоси {e}")
            await ctx.reply("или ффмпег установи хз")
            await voice_client.disconnect()
            return

        await asyncio.sleep(1)
        await self.play_random_sound(voice_client, prefix_include="countdown")

        members = voice_client.channel.members
        members = [m for m in members if m != ctx.bot.user]
        if len(members) >= 1:
            member = random.choice(members)
            self.last_kick = member
            # await asyncio.sleep(random.randint(1, 60))
            await member.move_to(None)
            await ctx.message.channel.send(f"хиххи хохо урод сосать рот молчать {member.mention}")
        else:
            await ctx.reply("уроды")

        await asyncio.sleep(5)
        await voice_client.disconnect()

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.last_kick and after.channel is None:
            await member.move_to(None)
        
    @Cog.listener()
    async def on_ready(self):
        print("Voice Kick Roulette cog loaded.")
