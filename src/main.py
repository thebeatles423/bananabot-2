import os

from dotenv import load_dotenv

from bot import bananabot

# load env file for bot token
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    # run bot
    bananabot.run(token=DISCORD_TOKEN)