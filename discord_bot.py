# discord_bot.py
import os
import sys
import discord
from discord import app_commands
from dotenv import load_dotenv
from g_sheets import GSheetsManager

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SPREADSHEET_KEY = os.getenv('SPREADSHEET_KEY')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', 'credentials.json')
GUILD_ID = os.getenv('GUILD_ID')

# Determine command prefix and dev mode based on "dev" argument
is_dev_mode = "dev" in sys.argv
command_prefix = "dev-" if is_dev_mode else ""

# Initialize Bot client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Initialize GSheetsManager as a global variable, to be instantiated on_ready
sheets_manager = None

# Event handler for when the bot is ready
@client.event
async def on_ready():
    global sheets_manager
    print("Initializing GSheetsManager...")
    sheets_manager = GSheetsManager(CREDENTIALS_PATH, SPREADSHEET_KEY)
    
    print(f'Logged in as {client.user}')
    
    if is_dev_mode:
        if not GUILD_ID:
            print("!!! FATAL ERROR: GUILD_ID is not set in .env file for dev mode.")
            return
        
        guild_obj = discord.Object(id=int(GUILD_ID))
        
        print(f"DEV MODE: Clearing and syncing commands for guild {GUILD_ID}...")
        tree.clear_commands(guild=guild_obj)
        await tree.sync(guild=guild_obj)
        print("Command tree synced to guild.")
    else:
        print("Syncing command tree globally...")
        await tree.sync()
        print("Command tree synced globally.")

# `/add` command
@tree.command(name=f"{command_prefix}add", description="Adds a new item to your list.")
@app_commands.describe(genre="The genre of the list", title="The title of the item")
async def add_item(interaction: discord.Interaction, genre: str, title: str):
    print(f"Received /{command_prefix}add command: genre='{genre}', title='{title}'")
    success = sheets_manager.add_item(genre, title)
    if success:
        await interaction.response.send_message(f"Added '{title}' to the **{genre}** list.")
    else:
        await interaction.response.send_message("Sorry, something went wrong while adding the item. Please check the bot's console for errors.", ephemeral=True)

# `/done` command
@tree.command(name=f"{command_prefix}done", description="Marks an item as completed.")
@app_commands.describe(genre="The genre of the list", title="The title of the item")
async def mark_as_done(interaction: discord.Interaction, genre: str, title: str):
    print(f"Received /{command_prefix}done command: genre='{genre}', title='{title}'")
    success = sheets_manager.mark_as_done(genre, title)
    if success:
        await interaction.response.send_message(f"Marked '{title}' in **{genre}** as completed.")
    else:
        await interaction.response.send_message(f"Could not find or update '{title}'. Please check the title and genre, or see the console for errors.", ephemeral=True)

# `/list` command
@tree.command(name=f"{command_prefix}list", description="Displays all items from a specified list.")
@app_commands.describe(genre="The genre of the list to display")
async def get_list(interaction: discord.Interaction, genre: str):
    print(f"Received /{command_prefix}list command: genre='{genre}'")
    items = sheets_manager.get_list(genre)
    
    if items is None: # Explicit check for error from get_list
        await interaction.response.send_message("Sorry, something went wrong while fetching the list. Please check the bot's console for errors.", ephemeral=True)
        return

    if not items:
        await interaction.response.send_message(f"The **{genre}** list is empty.")
        return

    embed = discord.Embed(title=f"{genre} List", color=0x00ff00)
    for item in items:
        status = item.get('Status', 'N/A')
        title = item.get('Title', 'N/A')
        embed.add_field(name=title, value=f"Status: {status}", inline=False)
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == '__main__':
    if not DISCORD_TOKEN or not SPREADSHEET_KEY:
        print("!!! FATAL ERROR: DISCORD_TOKEN or SPREADSHEET_KEY is not set in .env file.")
    else:
        print("Starting bot...")
        client.run(DISCORD_TOKEN)
