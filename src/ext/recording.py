import datetime

import discord
from discord.ext import commands


class Recording(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.connections = {} # vc's the bot is connected to
        self.recording = False

    # when the recording is done; callback function
    async def once_done(self, sink: discord.sinks, channel: discord.TextChannel, *args):
        recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
        
        await sink.vc.disconnect()

        file_name = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M.{sink.encoding}")
        files = [discord.File(audio.file, file_name) for user_id, audio in sink.audio_data.items()]

        # save file to local disk
        #with open(f"./recordings/{file_name}", 'wb') as file:
            #file.write(audio.file.getbuffer())
        
        return await channel.send(f"Audio recording saved as {file_name}", files=files)

    @commands.slash_command(name="join", description="Make the bot join the voice channel you're in")
    async def join(self, ctx):
        voice = ctx.author.voice
        
        if ctx.guild.id in self.connections:
            return await ctx.send_response("I'm already in a voice channel!", ephemeral=True)
        elif not voice:
            return await ctx.send_response(content="You aren't in a voice channel!", ephemeral=True)
        else:
            vc = await voice.channel.connect()
            self.connections.update({ctx.guild.id: [vc]})
            return await ctx.send_response(content="<embed here>") # TODO

    @commands.slash_command(name="leave", description="Leave the current voice channel. Stops any active recordings.")
    async def leave(self, ctx):
        voice = ctx.author.voice
        if self.recording:
            return stop_recording(ctx, leave=True)
        if ctx.guild.id not in self.connections:
            return await ctx.send_response("I'm not in a voice channel!", ephemeral=True)
        elif not voice:
            return await ctx.send_response("You need to be in the same voice channel as me to make me leave!", ephemeral=True)
        elif voice.channel.id != self.connections[ctx.guild.id][0].channel.id:
            return await ctx.send_response("You need to be in the same voice channel as me to make me leave!", ephemeral=True)
        else:
            del self.connections[ctx.guild.id]
            await ctx.delete()
            return await ctx.send_response("Leaving!")
    
    @commands.slash_command(name="record", description="Start recording the voice channel you're in")
    async def record(self, ctx):
        voice = ctx.author.voice

        if ctx.guild.id not in self.connections:
            return await ctx.send_response("I'm not in a voice channel!", ephemeral=True)
        elif not voice:
            return await ctx.send_response("You need to be in the same voice channel as me to record!", ephemeral=True)
        elif voice.channel.id != self.connections[ctx.guild.id][0].channel.id:
            return await ctx.send_response("You need to be in the same voice channel as me to record!", ephemeral=True)
        else:
            self.connections[ctx.guild.id][0].start_recording(discord.sinks.MP3Sink(), self.once_done, ctx.channel)
            self.connections[ctx.guild.id].append(ctx.author.id)

            self.recording = True
            return await ctx.send_response("Started recording!")

    @commands.slash_command(name="stop_recording", description="Stop an active recording")
    async def stop_recording(self, ctx, leave: bool):
        if ctx.guild.id in self.connections:
            if self.connections[ctx.guild.id][1] != ctx.author.id:
                return await ctx.send_response("You did not start this recording!", ephemeral=True)

            vc = self.connections[ctx.guild.id][0]
            vc.stop_recording()
            self.recording = False

            return await ctx.send_response("Stopped recording!")

            if leave:
                leave(ctx)
        else:
            return await ctx.respond("This server does not have an active recording!")


def setup(bot):
    bot.add_cog(Recording(bot))