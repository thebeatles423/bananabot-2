import discord
from discord.ext import commands
from googletrans import Translator

translator = Translator()


class TranslateView(discord.ui.View):
    def __init__(self, msglink):
        super().__init__()

        self.msglink = msglink

        link_button = discord.ui.Button(label="Message Link", style=discord.ButtonStyle.link, url=self.msglink)
        self.add_item(link_button)


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.message_command(name="Translate")
    async def translate(self, ctx, message: discord.Message):
        content = message.content
        translated = translator.translate(content, dest='en').text

        return await ctx.send_response(translated, view=TranslateView(message.jump_url))



def setup(bot):
    bot.add_cog(Translate(bot))