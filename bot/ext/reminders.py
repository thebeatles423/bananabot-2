import asyncio
import uuid
from datetime import datetime

import discord
from dateparser import parse
from discord.ext import commands

all_reminders = []

# for the buttons
class ReminderView(discord.ui.View):
    def __init__(self, msglink):
        super().__init__()

        self.msglink = msglink
        self.button = discord.ui.Button(label="Message Link", style=discord.ButtonStyle.link, url=self.msglink)

        self.add_item(self.button)


class Reminder:
    def __init__(self, ctx, msg: discord.Message, when: datetime, about, dm: bool, obj_id: uuid.UUID):
        self.ctx = ctx
        self.msg = msg
        self.when = when
        self.dm = dm
        self.obj_id = obj_id

        self.user = ctx.author

        if isinstance(about, discord.Message):
            self.about = str(self.about.content)
        else:
            self.about = about

    def find_wait_time(self):
        if self.when and datetime.now() < self.when:
            self.wait_time = (self.when - datetime.now()).seconds

            return self.wait_time
        else:
            raise ValueError("Invalid time")
    
    async def wait(self):
        wait_time = self.find_wait_time()
        await asyncio.sleep(wait_time)
        await self.remind()
    
    async def remind(self):
        if self.dm:
            await self.user.send(f"Reminder: {self.about}", view=ReminderView(self.msg.jump_url))
        else: # user has dms off
            await self.ctx.send_followup(f"<@{self.user.id}> Reminder: {self.about}", view=ReminderView(self.msg.jump_url))

        # remove reminder from all
        for index, rem in enumerate(all_reminders):
            if rem.obj_id == self.obj_id:
                del all_reminders[index]


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
        If the user can be DMed, 400 Bad Request is raised.
        If the user can't be DMed, 403 Forbidden is raised.
        """
        channel = user.dm_channel

        if channel is None:
            channel = await user.create_dm()

        try:
            await channel.send()
        except discord.Forbidden:
            return False
        except discord.HTTPException:
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

                msg = await ctx.send_response(f"Reminder set for {strtime}. Reason: {about}")
            else:
                dm = False

                response = f"Reminder set for {strtime}. Reason: {about}\n"
                response += "**NOTE: You have DMs off! Consider turning them on "
                response += "so I can remind you via DMs instead.**"

                msg = await ctx.send_response(response)

            msg = await msg.original_response()

            reminder_id = uuid.uuid4()

            reminder_object = Reminder(ctx=ctx, msg=msg, when=when, about=about, dm=dm, obj_id=reminder_id)
            await reminder_object.wait()

            self.all.append(reminder_object)
        except ValueError:
            return await ctx.send_response("Invalid time!")


def setup(bot):
    bot.add_cog(Reminders(bot))