import time
from datetime import datetime

import discord
from discord.ext import commands, tasks


class InfiniList(list):
    """A unique subclass of list that iterates infinitely"""
    def __init__(self):
        self.index = 0
    
    def __next__(self):
        if not len(self):
            return
        elif self.index == len(self) - 1:
            item = self[self.index]
            self.index = 0
        else:
            item = self[self.index]
            self.index += 1

        return item
    
    def append(self, item):
        if item not in self:
            super().append(item)


class Rotation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        self.nicknames = {}

        self.start()

    rotation = discord.SlashCommandGroup("rotation", "Rotate nicknames")

    @tasks.loop(hours=24)
    async def nick_loop(self):
        """Update usernames for users in rotation"""
        for user, nicks in self.nicknames.items():
            nick = next(nicks) or user.display_name
            await user.edit(nick=nick)

    def start(self):
        now = datetime.now()
        next_midnight = now.replace(
            day=now.day + 1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        self.nick_loop._next_iteration = next_midnight
        self.nick_loop.start()

    @rotation.command()
    async def add(
        self,
        ctx,
        user: discord.SlashCommandOptionType.user,
        nick: str
    ):
        if len(nick) > 32:
            return await ctx.send_response(
                "That nickname is too long!",
                ephemeral=True
            )
        elif user not in self.nicknames:
            self.nicknames[user] = InfiniList()
            self.nicknames[user].append(nick)
        else:
            self.nicknames[user].append(nick)
        
        await ctx.send_response(
            f"Added nickname `{nick}` for {user.mention}"
        )
    
    @rotation.command()
    async def remove(
        self,
        ctx,
        user: discord.SlashCommandOptionType.user,
        nick: str
    ):
        if user not in self.nicknames:
            return await ctx.send_response(
                "That user does not have any nicknames!",
                ephemeral=True
            )
        elif nick not in self.nicknames[user]:
            return await ctx.send_response(
                "That user does not have that nickname!",
                ephemeral=True
            )
        else:
            self.nicknames[user].remove(nick)
            return await ctx.send_response(
                f"Removed nickname `{nick}` for {user.mention}"
            )
    
    @rotation.command()
    async def view(
        self,
        ctx,
        user: discord.SlashCommandOptionType.user
    ):
        if user not in self.nicknames or not self.nicknames[user]:
            return await ctx.send_response(
                f"{user.mention} has no nicknames in rotation!",
                ephemeral=True
            )
        else:
            reply = f"{user.mention} has the following nicknames:\n"
            for nick in self.nicknames[user]:
                reply += f"`{nick}`\n"
            
            return await ctx.send_response(reply)


def setup(bot):
    bot.add_cog(Rotation(bot))