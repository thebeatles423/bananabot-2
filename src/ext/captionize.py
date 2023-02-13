import tempfile

import discord
import requests
import whisper
from discord.ext import commands

model = whisper.load_model("base")
print("Model loaded!")

class Captionize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="captionize")
    async def captionize(self, ctx, url: str):
        await ctx.defer()
        message: discord.Message = await ctx.send_followup("Downloading video...")

        video = requests.get(url)

        with tempfile.TemporaryDirectory() as tempd:
            with open(f"{tempd}/video.mp4", 'wb') as file:
                file.write(video.content)

            await message.edit("Transcribing video...")
            result = model.transcribe(f"{tempd}/video.mp4")
            
            with open(f"{tempd}/result.txt", 'w') as file:
                file.write(result["text"])
        
            return await message.edit(
                "Finished!",
                file=discord.File(f"{tempd}/result.txt")
            )


def setup(bot):
    bot.add_cog(Captionize(bot))