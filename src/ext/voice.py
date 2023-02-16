import datetime

import discord
from discord import SlashCommandGroup
from discord.ext import commands


class Voice(commands.Cog):
    voice = SlashCommandGroup("voice", "Voice channel commands")

    def __init__(self, bot):
        self.bot = bot

        self.connections = {} # vc's the bot is connected to

    @voice.command()
    async def join(self, ctx):
        voice = ctx.author.voice

        if not voice:
            return await ctx.send_response(
                "You aren't in a voice channel!",
                ephemeral=True
            )
        elif ctx.guild.id in self.connections:
            return await ctx.send_response(
                "I'm already in a voice channel!",
                ephemeral=True
            )
        else:
            vc = await voice.channel.connect()

            vc.inviter = ctx.author
            self.connections.update({ctx.guild.id: vc})

            return await ctx.send_response(f"Joined <#{vc.channel.id}>!")

    @voice.command()
    async def leave(self, ctx):
        voice = ctx.author.voice

        if not voice:
            return await ctx.send_response(
                "You aren't in a voice channel!",
                ephemeral=True
            )
        elif ctx.guild.id not in self.connections:
            return await ctx.send_response(
                "I'm not in a voice channel!",
                ephemeral=True
            )
        elif ctx.author != self.connections[ctx.guild.id].inviter:
            return await ctx.send_response(
                "You did not invite me to this voice channel!",
                ephemeral=True
            )
        else:
            vc = self.connections[ctx.guild.id]
            # if recording, stop

            await vc.disconnect()
            del self.connections[ctx.guild.id]

            return await ctx.send_response(f"Left <#{vc.channel.id}>!")
    
    @voice.command()
    async def record(self, ctx):
        ...


def setup(bot):
    bot.add_cog(Voice(bot))