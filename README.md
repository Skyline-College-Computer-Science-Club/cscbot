# Skyline College Computer Science Bot (we don't a name yet)!

## How to Install & Run

### Preparations

Install the following:

1. Git (https://git-scm.com/downloads)
2. Python (https://www.python.org/downloads/)
3. A text editor of your choice (I prefer VSCode: https://code.visualstudio.com/download)

Next, set up Discord developer credentials: https://discord.com/developers/applications

Create an application by clicking `New Application` at the top-right, click `Bot`, and click `Add Bot`. Next, get your token and paste it somewhere safe. We will be needing it soon!

Finally, create a server for personal bot development. This is where your bot will be located.

### Adding the bot to your server

You can add your bot by clicking on `OAuth2` and then `URL Generator`. Under `scopes`, click the checkbox for `bot`. Scroll down, and click `Administrator` under `Bot Permissions`

Paste the generated URL into your browser and invite your bot to your server.

### Set up Local Developer Environment

```
git clone https://github.com/johncmanuel/cscbot
cd cscbot
```

#### Install a Python virtual environment and activate it:

```
py -m venv .
cd Scripts
activate
cd ..
```

#### Install the required packages:

```
pip install -r requirements.txt
```

#### Create .env file and paste the following:

```
DISCORD_TOKEN=<your token>
DISCORD_GUILD=<name of your bot development server>
```

### Running the bot

```
py bot.py
```

The bot should be running in your server. Now it is time to start developing! Consult the Internet and/or the documentation below for more information on Discord bots.

#### discord.py documentation:

https://discordpy.readthedocs.io/en/stable/
