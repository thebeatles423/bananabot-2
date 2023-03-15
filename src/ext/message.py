import discord
from discord.ext import commands


class ReadView(discord.ui.View):
    def __init__(self, msglink):
        super().__init__()

        self.msglink = msglink

        link_button = discord.ui.Button(label="Message Link", style=discord.ButtonStyle.link, url=self.msglink)
        self.add_item(link_button)


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


class ReactModal(discord.ui.Modal):
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
            label="Emoji",
            style=discord.InputTextStyle.short
            )
        )
    
    async def callback(self, interaction: discord.Interaction):
        reaction = self.children[0].value
        try:
            await self.message.add_reaction(reaction)
        except Exception as e:
            return await interaction.response.send_message(
                f"Failed to add reaction!\n```{e}```",
                ephemeral=True
            )

        return await interaction.response.send_message(
            "Added reaction!",
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
    

class Message(commands.Cog):
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

    @commands.message_command(name="React")
    @commands.is_owner()
    async def react(self, ctx, message: discord.Message):
        return await ctx.send_modal(
            ReactModal(message, title="React to message:")
        )

    # max 5 message commands 
    # @commands.message_command(name="Read")
    # async def read(self, ctx, message: discord.Message):
    #     content = message.content
    #     response = "```\n{}\n```".format(content.replace('`', r'\`'))

    #     return await ctx.send_response(response, view=ReadView(message.jump_url))



def setup(bot):
    bot.add_cog(Message(bot))