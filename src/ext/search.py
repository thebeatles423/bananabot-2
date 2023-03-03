import io

import discord
import pytesseract
from discord.ext import commands
from PIL import Image


class MessageView(discord.ui.View):
    def __init__(self, msglink):
        super().__init__()

        self.msglink = msglink

        link_button = discord.ui.Button(
            label="Message Link",
            style=discord.ButtonStyle.link,
            url=self.msglink
        )

        self.add_item(link_button)


class Search(commands.Cog):
    #search = SlashCommandGroup()

    def __init__(self, bot):
        self.bot = bot

    @commands.message_command(name="Image Text")
    async def image_text(self, ctx, message: discord.Message):
        images = [
            attachment for attachment in message.attachments
            if "image/" in attachment.content_type
        ]
        if not images:
            return await ctx.send_response(
                "That message does not contain an image!",
                ephemeral=True
            )
        else:
            read_images = [
                io.BytesIO(await image.read()) for image in images
            ]

            for image in read_images:
                await ctx.send_response(
                    f"```{pytesseract.image_to_string(Image.open(image))}```",
                    view=MessageView(message.jump_url)
                )


def setup(bot):
    bot.add_cog(Search(bot))