"""
This really needs to be refactored so I'm going to put some notes for myself here:

- The remindme command freezes at reminder.wait(), idk why
- There needs to be a better system for waiting ^
- Snooze button *technically* works but again it uses some code from the remindme command
Building off of that, it would be easier to have a streamlined process rather
than having a lot of the reminder code in the Reminders cog/remindme command
"""


import asyncio
import uuid
from datetime import datetime

import discord
from dateparser import parse
from discord.ext import commands

all_reminders = []

# for the buttons
class ReminderView(discord.ui.View):
    def __init__(self, ctx, msglink, reminder):
        super().__init__()

        self.ctx = ctx
        self.msglink = msglink
        self.reminder = reminder

        self.link_button = discord.ui.Button(label="Message Link", style=discord.ButtonStyle.link, url=self.msglink)

        self.add_item(self.link_button)

    @discord.ui.button(label="Snooze", style=discord.ButtonStyle.red, emoji="⏰")
    async def button_callback(self, button, interaction):
        # see __str__ method of Reminder class for self.reminder
        await interaction.response.send_modal(SnoozeModal(ctx=self.ctx, reminder=self.reminder, title="Snooze"))

# request user for time to snooze (used above)
class SnoozeModal(discord.ui.Modal):
    def __init__(self, ctx, reminder, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ctx = ctx
        self.reminder = reminder

        self.add_item(discord.ui.InputText(label="When do you want to be reminded?"))
    
    async def callback(self, interaction: discord.Interaction):
        self.snoozetime = self.children[0].value
        self.snoozetime = parse(self.snoozetime)
        try:
            await self.reminder.snooze(self.snoozetime)
            await self.ctx.followup.send("Snoozed reminder!", ephemeral=True)
        except ValueError:
            await self.ctx.followup.send("Invalid time!", ephemeral=True)


class Reminder:
    def __init__(self, ctx, msg: discord.Message, when: datetime, about, dm: bool):
        self.ctx = ctx
        self.msg = msg
        self.when = when
        self.dm = dm

        self.user = ctx.author

        if isinstance(about, discord.Message):
            self.about = str(self.about.content)
        else:
            self.about = about

    def find_wait_time(self):
        if self.when is None:
            raise ValueError("Invalid time!")
        if self.when and datetime.now() < self.when:
            self.wait_time = (self.when - datetime.now()).seconds
        else:
            raise ValueError("Invalid time")
    
    async def wait(self):
        self.find_wait_time()
        await asyncio.sleep(self.wait_time)
        await self.remind()
    
    async def remind(self):
        if self.dm:
            await self.user.send(f"Reminder: {self.about}", view=ReminderView(self.ctx, self.msg.jump_url, self))
        else: # user has dms off
            await self.ctx.send_followup(
                f"<@{self.user.id}> Reminder: {self.about}", 
                view=ReminderView(self.ctx, self.msg.jump_url, self)
                )
    
    async def snooze(self, when: str):
        # if the time is invalid (determined later)
        # we want to restore the original reminder time
        old_when = self.when # store old time
        self.when = when # set when to new time
        
        await self.wait()


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        # if there are reminders saved to disk, load them --
        # these are stored if the bot shuts down and reminders
        # need to be saved
        try:
            with open("./all.pkl", 'rb') as file:
                ...
        except FileNotFoundError:
            self.all = []
        
        # handle any expired reminders
        for reminder in self.all:
            ...

    def save_all(self):
        ...

    async def can_dm(self, user: discord.User) -> bool:
        """
        Determine if a user can be DMed.

        This works by sending an invalid DM. 
        If the user can't be DMed, 403 Forbidden is raised.
        If the user can be DMed, 400 Bad Request is raised.

        `except discord.Forbidden` must come first!! because
        discord.Forbidden is a subclass of discord.HTTPException
        """
        channel = user.dm_channel

        if channel is None:
            channel = await user.create_dm()

        try:
            await channel.send()
        except discord.Forbidden: # 403 Forbidden
            return False
        except discord.HTTPException as e: # 400 Bad Request
            return True
        
    @commands.slash_command(name="remindme", description="Have the bot remind you about something, via DMs")
    async def remindme(self, ctx, when: str, about: discord.Option(str, required=False, default='')):
        # parse input to datetime object
        # returns None if input could not be parsed
        when: datetime.datetime = parse(when)
        strtime = when.strftime("%Y-%m-%d %H:%M:%S")

        if not about:
            about = "[no reason provided]"

        try:
            if await self.can_dm(ctx.author):
                dm = True

                msg = await ctx.send_response(f"Reminder set for {strtime}. Reason: {about}", ephemeral=True)
            else:
                dm = False

                response = f"Reminder set for {strtime}. Reason: {about}\n"
                response += "**NOTE: You have DMs off! Consider turning them on "
                response += "so I can remind you via DMs instead.**"

                msg = await ctx.send_response(response)

            msg = await msg.original_response()

            reminder = Reminder(ctx, msg, when, about, dm)
            await reminder.wait()
            all_reminders.append(reminder)
        except ValueError:
            return await ctx.send_response("Invalid time!")


def setup(bot):
    bot.add_cog(Reminders(bot))