import discord
from discord.ext import commands
from discord import NotFound


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="listexts", description="List loaded extensions.")
    @commands.is_owner()
    async def listexts(self, ctx):
        reply = ["Loaded extensions:"]
        for extension in self.bot.extensions:
            reply.append(f"`{extension}`")
        reply = '\n'.join(reply)

        return await ctx.send_response(content=reply, ephemeral=True)

    @commands.slash_command(name="reloadext", description="Reload extension by name.")
    @commands.is_owner()
    async def reloadext(self, ctx, extension: str):
        try:
            self.bot.reload_extension(extension)
            return await ctx.send_response(content=f"Reloaded extension `{extension}`", ephemeral=True)
        except: # fix this to not be bare except at some point - may cause problems
            return await ctx.send_response(content=f"Extension `{extension}` has not been loaded!", ephemeral=True)
    
    @commands.slash_command(name="send", description="Make the bot send a message.")
    @commands.is_owner()
    async def send(self, ctx, message):
        await ctx.send_response("Message sent!", ephemeral=True)
        return await ctx.send(message)
    
    @commands.slash_command(name="read", description="Show what text the bot sees in a message.")
    @commands.is_owner()
    async def read(self, ctx, message_id, ephemeral: bool = True, format_as_code: bool = True):
        message = None
        if '-' in message_id: # both channel ID and message ID were copied: <channel_id>-<message_id>
            for guild in self.bot.guilds:
                try:
                    channel = guild.get_channel(int(message_id.split('-')[0]))
                except NotFound:
                    continue
                try:
                    message = await channel.fetch_message(int(message_id.split('-')[1]))
                except:
                    message = None
        else: # only message ID was copied
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    try:
                        message = await channel.fetch_message(int((message_id)))
                    except NotFound:
                        continue
            
        if not message: # if the message wasn't found
            return await ctx.send_response("The message could not be found!", ephemeral=True)
        
        message = str(message.content)
        if format_as_code:
            message = message.replace('`', r'\`')
            response = "```\n{}\n```".format(message)
        else:
            response = message
        
        return await ctx.send_response(response, ephemeral=ephemeral)


def setup(bot):
    bot.add_cog(Debug(bot))