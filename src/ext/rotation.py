import asyncio
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks


class Rotation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        self.nicknames = {
            "Monday": {},
            "Tuesday": {},
            "Wednesday": {},
            "Thursday": {},
            "Friday": {},
            "Saturday": {},
            "Sunday": {}
        }

    rotation = discord.SlashCommandGroup("rotation", "Rotate nicknames")

    @tasks.loop(hours=24)
    async def nick_loop(self):
        """Update usernames for users in rotation"""
        to_change_today = self.nicknames[datetime.today().strftime('%A')]
        for user, nick in to_change_today.items():
            await user.edit(nick=nick)

    async def restart(self):
        now = datetime.now()
        next_midnight = now.replace(
            day=now.day + 1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        wait_time = next_midnight - now

        # wait for the next day
        await asyncio.sleep(wait_time.seconds + 5)
        self.nick_loop.cancel()
        self.nick_loop.start()

    async def days(ctx: discord.AutocompleteContext):
        return [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

    @rotation.command()
    async def add(
        self, ctx,
        user: discord.SlashCommandOptionType.user,
        when: discord.Option(
            str,
            autocomplete=discord.utils.basic_autocomplete(days)
        ),
        nick: str
    ):
        if when not in await self.days():
            return await ctx.send_response(
                "Invalid date!",
                ephemeral=True
            )
        elif len(nick) > 32:
            return await ctx.send_response(
                "Nickname provided is too long!",
                ephemeral=True
            )
        else:
            self.nicknames[when].update({user: nick}) 
            await ctx.send_response(
                f"Nickname `{nick}` for {user.mention} added on **{when}**"
            )

            return await self.restart()


def setup(bot):
    bot.add_cog(Rotation(bot))