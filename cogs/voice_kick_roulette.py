import discord.ext.commands as commands
import os.path as path
import os
import asyncio
import random
import discord


class VoiceKickRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_kick = None
        self.sounds = os.listdir(
            path.join(os.getcwd(), "sounds", "voice_kick_roulette")
        )
        self.bot.loop.create_task(self.kick_all_loop())

    # @commands.is_owner()
    @commands.command(name="ls")
    async def list_sounds(self, ctx: commands.Context):
        """List all sounds available for the voice kick roulette."""
        sounds = (
            ", ".join(self.sounds) if self.sounds else "хихихи хохохо нищий без звуков"
        )
        await ctx.reply(sounds)

    async def play_random_sound(
        self,
        vc: discord.VoiceClient,
        n: int = 1,
        prefix_include: str = None,
        prefix_exclude: str = None,
    ):
        sounds = (
            [s for s in self.sounds if s.startswith(prefix_include)]
            if prefix_include
            else self.sounds
        )
        sounds = (
            [s for s in sounds if not s.startswith(prefix_exclude)]
            if prefix_exclude
            else sounds
        )
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

    @commands.command(name="allahukbar")
    async def kick_all_cmd(self, ctx: commands.Context):
        await self.kick_all(ctx.author.voice.channel)

    async def kick_all(self, voice_channel: discord.VoiceChannel):
        """Kick all members from the voice channel."""
        await voice_channel.connect()
        voice_client = voice_channel.guild.voice_client
        try:
            await self.play_random_sound(voice_client, prefix_include="short")
        except Exception as e:
            await print(f"{e}")
            await voice_client.disconnect()
            return

        members = voice_client.channel.members
        for member in members:
            if member != self.bot.user:
                await member.move_to(None)
                # await asyncio.sleep(0.1)

        await asyncio.sleep(5)
        await voice_client.disconnect()

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
            await ctx.message.channel.send(
                f"хиххи хохо урод сосать рот молчать {member.mention}"
            )
        else:
            await ctx.reply("уроды")

        await asyncio.sleep(5)
        await voice_client.disconnect()

    # function that calls kick_all every 5 minutes
    async def kick_all_loop(self):
        await self.bot.wait_until_ready()
        all_voice_channels = self.bot.get_all_channels()
        voice_channels = [c for c in all_voice_channels if isinstance(c, discord.VoiceChannel)]
        while not self.bot.is_closed():
            await asyncio.sleep(random.randint(120, 900))
            # await self.bot.get_channel(1113155133791027202).send("хихихи хохохо")
            # kick all members from a voice with the most members
            voice_channels.sort(key=lambda c: len(c.members), reverse=True)
            if voice_channels:
                # if random.random() < -0.1:
                #     await self.kick_all(voice_channels[0])
                # else:
                vc = await voice_channels[0].connect()
                # await self.play_random_sound(vc, 1, prefix_include="short")
                await asyncio.sleep(1)
                await vc.disconnect()

            # await asyncio.sleep(random.randint(300, 1800))
