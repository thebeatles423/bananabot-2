import os
import pickle
from pathlib import Path

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

        self.SAVE_DIR = os.path.join(
            Path.home(),
            ".cache",
            "bananabot"
        )
        self.SAVE_FP = os.path.join(self.SAVE_DIR, "nicknames.pkl")

        self.nick_loop.start()

    rotation = discord.SlashCommandGroup("rotation", "Rotate nicknames")

    @tasks.loop(hours=24)
    async def nick_loop(self):
        """Update usernames for users in rotation"""

        for user, nicks in self.nicknames.items():
            nick = next(nicks) or user.display_name
            await user.edit(nick=nick)

    @nick_loop.before_loop
    async def before_nick_loop(self):
        await self.bot.wait_until_ready()

        await self.load_nicknames()
        await self.update_nicknames()

    def save_nicknames(self):
        self.id_nicknames = {}
        
        for user, nicks in self.nicknames.items():
            self.id_nicknames[user.id] = nicks
        
        with open(self.SAVE_FP, 'wb') as file:
            pickle.dump(self.id_nicknames, file)

    async def load_nicknames(self):
        if not os.path.isdir(self.SAVE_DIR):
            os.mkdir(self.SAVE_DIR)
            self.nicknames = {}
        elif not (os.path.isfile(self.SAVE_FP)):
            self.nicknames = {}
        else:
            with open(self.SAVE_FP, 'rb') as file:
                self.nicknames = {}
                self.id_nicknames = pickle.load(file)
    
    async def update_nicknames(self):
        for userid, nicks in self.id_nicknames.items():
            for member in self.bot.get_all_members():
                if member.id == userid:
                    user = member
                    
            self.nicknames[user] = nicks


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

        self.save_nicknames()
    
    @rotation.command()
    async def remove(
        self,
        ctx,
        user: discord.SlashCommandOptionType.user,
        nick: str
    ):
        if user not in self.nicknames:
            await ctx.send_response(
                "That user does not have any nicknames!",
                ephemeral=True
            )
        elif nick not in self.nicknames[user]:
            await ctx.send_response(
                "That user does not have that nickname!",
                ephemeral=True
            )
        else:
            self.nicknames[user].remove(nick)
            await ctx.send_response(
                f"Removed nickname `{nick}` for {user.mention}"
            )
        
        return self.save_nicknames()
    
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
    
    @rotation.command()
    async def next(self, ctx):
        return await ctx.send_response(
            f"Next iteration: <t:{round(self.nick_loop.next_iteration.timestamp())}:R>",
            ephemeral=True
        )
    
    @commands.is_owner()
    @rotation.command()
    async def set(
        self,
        ctx,
        days: discord.Option(int, default=0),
        hours: discord.Option(int, default=0),
        minutes: discord.Option(int, default=0),
        seconds: discord.Option(int, default=0)
    ):  
        if any(x < 0 for x in (hours, minutes, seconds)):
            return await ctx.send_response(
                "Invalid time!",
                ephemeral=True
            )

        adjusted_hours = hours + days * 24
        self.nick_loop.change_interval(
            hours=adjusted_hours,
            minutes=minutes,
            seconds=seconds
        )

        response = f"Set rotation interval to: {days} days, {hours}:{minutes}:{seconds}"
        
        await ctx.send_response(response, ephemeral=True)

        self.nick_loop.restart()


def setup(bot):
    bot.add_cog(Rotation(bot))