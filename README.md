# Bananabot
A Discord bot with various utilities and other features that I may or may not use in the future

## Invite
If you'd like, you can invite the bot by clicking on [this](https://discord.com/api/oauth2/authorize?client_id=970138406879395930&permissions=8&scope=bot) link

## Installation
You can also self host the bot for your own purposes:
* Clone the repository:
```
git clone https://github.com/kbidlack/bananabot.git
```
* Navigate to the newly created directory:
```
cd bananabot
```
* Optional: Create a virtual environment to install the packages to:
```
python -m venv env
. env/bin/activate
```
* Install the dependencies:
```
pip install -Ur requirements.txt
```
* Create a file called `.env` and put your bot token in it like this:
```
DISCORD_TOKEN="<your_token_here>"
```
* Run the bot!
```
python bot/main.py
```