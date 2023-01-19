import discord
import requests
from discord.ext import commands


class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        name="define",
        description="Define a word (using https://dictionaryapi.dev)"
    )
    async def define(self, ctx, word: str):
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        
        if response.status_code != 200:
            return await ctx.send_response(f"Couldn't find a definition for the word '{word}'")
        elif 'title' in response.json():
            return await ctx.send_response(f"Couldn't find a definition for the word '{word}'")

        response_json = response.json()[0]

        # create embed
        if not response_json['phonetics']:
            pronunciation = "None"
        else:
            pronunciation = [
                d for d in response_json['phonetics'] if 'text' in d
            ][0]['text']

        embed = discord.Embed(
            title=f'Definition of "{word}"',
            description=f"Pronunciation: {pronunciation}",
            color=discord.Colour.green(),
        )

        for meaning in response_json['meanings']:
            definitions = [
                f"{index + 1}. {definition['definition']}"
                for index, definition in enumerate(meaning['definitions'])
            ]
            
            definitions_string = ""

            for definition in definitions:
                definitions_string += (definition + '\n')
    
            embed.add_field(
                name=meaning['partOfSpeech'],
                value=f"_Definitions:_\n{definitions_string}",
                inline=False
            )
        
        return await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Define(bot))