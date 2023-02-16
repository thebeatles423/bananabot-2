import discord
from discord import NotFound
from discord.ext import commands


class EditModal(discord.ui.Modal):
    def __init__(
        self, 
        message: discord.Message,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.message = message
        
        self.add_item(
            discord.ui.InputText(
                label="Message",
                style=discord.InputTextStyle.long,
                value=self.message.content
            )
        )
    
    async def callback(self, interaction: discord.Interaction):
        content = self.children[0].value
        await self.message.edit(content)
        return await interaction.response.send_message(
            "Edited message!",
            ephemeral=True
        )


class ReplyModal(discord.ui.Modal):
    def __init__(self, message: discord.Message, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = message

        self.add_item(
            discord.ui.InputText(
                label="Message", style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        content = self.children[0].value
        await self.message.reply(content)
        return await interaction.response.send_message(
            "Replied to message!",
            ephemeral=True
        )


class ReadView(discord.ui.View):
    def __init__(self, msglink):
        super().__init__()

        self.msglink = msglink

        link_button = discord.ui.Button(label="Message Link", style=discord.ButtonStyle.link, url=self.msglink)
        self.add_item(link_button)


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="listexts", description="List loaded extensions")
    @commands.is_owner()
    async def listexts(self, ctx):
        reply = ["Loaded extensions:"]
        for extension in self.bot.extensions:
            reply.append(f"`{extension}`")
        reply = '\n'.join(reply)

        return await ctx.send_response(content=reply, ephemeral=True)

    @commands.slash_command(name="reloadext", description="Reload extension by name")
    @commands.is_owner()
    async def reloadext(self, ctx, extension: str):
        try:
            self.bot.reload_extension(extension)
            return await ctx.send_response(content=f"Reloaded extension `{extension}`", ephemeral=True)
        except:
            return await ctx.send_response(content=f"Extension `{extension}` has not been loaded!", ephemeral=True)

    @commands.slash_command(name="loadext", description="Load an extension")
    @commands.is_owner()
    async def loadext(self, ctx, extension: str):
        try:
            self.bot.load_extension(extension)
            return await ctx.send_response(content=f"Loaded extension `{extension}`", ephemeral=True)
        except:
            return await ctx.send_response(content=f"An error occurred while trying to load extension `{extension}`", ephemeral=True)
    
    @commands.slash_command(name="send", description="Make the bot send a message")
    @commands.is_owner()
    async def send(self, ctx, message):
        await ctx.send_response("Message sent!", ephemeral=True)
        return await ctx.send(message)

    @commands.message_command(name="Reply", description="Make the bot reply to a message")
    @commands.is_owner()
    async def reply(self, ctx, message: discord.Message):
        modal = ReplyModal(message, title="Message to reply with:")
        return await ctx.send_modal(modal)
    
    @commands.message_command(name="Edit", description="Edit a message the bot has sent")
    @commands.is_owner()
    async def edit(self, ctx, message: discord.Message):
        try:
            return await ctx.send_modal(
                EditModal(message, title="Edit message:")
            )
        except discord.HTTPException:
            return await ctx.send_response(
                "I can't edit this message!",
                ephemeral=True
            )
    
    @commands.message_command(name="Read")
    async def read(self, ctx, message: discord.Message):
        content = message.content
        response = "```\n{}\n```".format(content.replace('`', r'\`'))

        return await ctx.send_response(response, view=ReadView(message.jump_url))


def setup(bot):
    bot.add_cog(Debug(bot))
