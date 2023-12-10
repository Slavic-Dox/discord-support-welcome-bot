import subprocess

# Installation der erforderlichen Pakete
subprocess.run(['pip', 'install', 'discord'])
subprocess.run(['pip', 'install', 'python-dotenv'])


import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="DM für Support"))

@bot.event
async def on_member_join(member):
    # ID des Kanals, in dem die Willkommensnachricht gesendet werden soll
    channel_id = #0815
    
    # Text der Willkommensnachricht
    welcome_message = f'Willkommen {member.mention} auf diesem Server!'
    
    # Sucht den Kanal anhand der ID
    channel = bot.get_channel(channel_id)
    
    # Sendet die Willkommensnachricht in den Kanal
    await channel.send(welcome_message)

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        # Erstellt einen neuen Textkanal im Server des Bots
        guild = bot.get_guild(876543210)  # ID des Servers, auf dem der Kanal erstellt werden soll
        category_id = 10987654321 # ID der Kategorie, in der der Kanal erstellt werden soll
        channel_name = f'support-{message.author.name}'
        
        # Rollen-ID angeben
        support_role_id = 1234567890
        
        # Überprüft, ob die Support-Rolle vorhanden ist
        support_role = guild.get_role(support_role_id)
        if support_role is None:
            return
        
        # Sucht die Kategorie anhand der ID
        category = discord.utils.get(guild.categories, id=category_id)
        if category is None:
            return
        
        # Berechtigungen für den neuen Kanal
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True),
            support_role: discord.PermissionOverwrite(read_messages=True)
        }
        
        # Erstellt den neuen Kanal in der Kategorie
        new_channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        # Sendet eine Begrüßungsnachricht im neuen Kanal
        welcome_message = f'Hallo {message.author.mention}, willkommen in deinem Support-Kanal!'
        await new_channel.send(welcome_message)

        # Leitet die Nachricht des Benutzers in den neuen Kanal weiter
        forwarded_message = f'**Ticket von:** {message.author.mention}\n{message.content}'
        await new_channel.send(forwarded_message)

    await bot.process_commands(message)

# Token des Discord-Bots
token = 'IHR BOT TOKEN'

# Startet den Bot
bot.run(token)
