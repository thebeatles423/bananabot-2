import discord
from discord.ext import commands
from googletrans import Translator
from googletrans import LANGUAGES

translator = Translator()


class TranslateView(discord.ui.View):
    def __init__(self, msglink, src_lang: str):
        super().__init__()

        link_button = discord.ui.Button(label=f"Message Link ({src_lang})", style=discord.ButtonStyle.link, url=msglink)
        self.add_item(link_button)


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.message_command(name="Translate")
    async def translate(self, ctx, message: discord.Message):
        content = message.content

        translated = translator.translate(content, dest='en')
        translated_text = translated.text
        src_lang = LANGUAGES[translated.src].capitalize()

        return await ctx.send_response(
            translated_text,
            view=TranslateView(message.jump_url, src_lang),
        )



def setup(bot):
    bot.add_cog(Translate(bot))