import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from discord.ext import tasks
import os
from dotenv import load_dotenv
rolled = {}
money = {}
load_dotenv()
user_inventory = {}
all_fruits = ["rocket", "spin", "blade", "spring", "bomb", "smoke", "spike", "flame", "dark", "sand", "ice", "rubber", "eagle", "ghost", "light", "diamond", "quake", "magma", "love", "spider", "sound", "phoenix", "creation", "blizzard", "buddha", "portal", "venom", "spirit", "mammonth", "gravity", "trex", "pain", "dough", "lightning", "tiger", "gas"," yeti", "kitsune", "control", "dragon", "dragonwest", "dragoneast"]
fruit_prices = {
    # Common (সস্তা)
    "rocket": 500, "spin": 1200, "blade": 2000, "spring": 3500, "bomb": 5000, 
    "smoke": 7000, "spike": 8500, "gas": 10000, "yeti": 12000,
    
    # Uncommon (মাঝারি)
    "flame": 25000, "dark": 30000, "sand": 35000, "ice": 40000, "rubber": 50000, 
    "eagle": 55000, "ghost": 65000, "light": 80000, "diamond": 90000,
    
    # Rare & Legendary (দামী)
    "quake": 120000, "magma": 150000, "love": 180000, "spider": 200000, 
    "sound": 220000, "phoenix": 250000, "creation": 280000, "blizzard": 320000, 
    "buddha": 400000, "portal": 450000,
    
    # Mythical (ভয়ংকর দামী)
    "venom": 600000, "spirit": 750000, "mammonth": 850000, "gravity": 900000, 
    "trex": 1000000, "pain": 1100000, "dough": 1500000, "lightning": 1800000, 
    "tiger": 2000000, "kitsune": 3000000, "control": 3500000, "dragon": 4000000, 
    "dragonwest": 4500000, "dragoneast": 4500000
}
fruits_weight = [
    100, 100, 98, 97, 96, 96, 96, 94, # Common (8)
    89, 89, 81, 83, 83, 85, 80, 73,   # Rare (8)
    80, 70, 70, 68, 69, 63, 70, 63,   # Epic/Legendary (8)
    70, 54, 54, 54, 54, 54, 54, 45,   # Mythical/High (8)
    53, 40, 35, 2,                     # Next set (4)
    53, 40, 35, 6, 4, 0.01
]
current_stock = ["rocket", "spin", "blade"] #So, I don't need to wait for 3hours
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=["!", "?", ".", "$"], intents=intents)
wChannel = {}
lChannel = {}

@bot.event
async def on_ready():
    try:
        synched = await bot.tree.sync()
        print(f"Bot is online! Logged in as {bot.user.name}")
        print(f"Loaded {len(synched)} commands successfully!")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="All members!"))
        
    except Exception as e:
        print(f"Can't load commands! error:\n{e}")
@bot.event
async def on_member_join(member):
    guild = member.guild
    guild_id = guild.id
    channel_id = wChannel.get(guild_id)
    channel = bot.get_channel(channel_id)
    try:
        if guild_id in wChannel:
            await channel.send(f"{member.mention} just joined the server! We have now {guild.member_count} members!")
        else: return
    except Exception as e:
        print(f"Something went wrong!\n{e}")
@bot.event
async def on_message_delete(message):
    guild = message.guild
    guildId = guild.id
    
    channels =lChannel.get(guildId)
    try:
        if guildId in lChannel:
            if message.author.bot:
                return
            else:
                embed = discord.Embed(
                    color=0xADD8E6,
                    title="Message deleted"
                )
                embed.add_field(name="``author``", value=message.author)
                embed.add_field(name="``channel``", value=message.channel.mention)
                await channels.send(embed=embed)
    except Exception as e:
        print(f"Something went wrong! error:\n{e}")
@bot.tree.command(name="setweclome", description="set a channel for welcome")
@app_commands.describe(channel="pls enter a channel")
async def setwelcome(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        serverId = interaction.guild.id
        wChannel[serverId] = channel.id
        await interaction.response.send_message(f"Setted welcome channel in {channel.id}!")
    except Exception as e:
        print(f"Something went wrong!\n{e}")
@bot.tree.command(name="setlog", description="set a log channel for delette message log")
@app_commands.describe(channel="pls select a channel")
async def setlog(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        serverid = interaction.guild.id
        lChannel[serverid] = channel
        await interaction.response.send_message(f"Successfully added log channels to {channel.id}!")
    except Exception as e:
        print("Something went wrong! Error:\n", e)
@bot.tree.command(name="isfruits", description="type a fruits name and search that is it fruit or not")
@app_commands.describe(fruit="pls type a fruit name")
async def isfruits(interaction: discord.Interaction, fruit:str):
    fruits = fruit.replace("-", "")
    if fruits.lower() in all_fruits:
        await interaction.response.send_message("Is is a fruits in blox fruits!")
    else:
        await interaction.response.send_message("It is not a fruits in blox fruits!")
@bot.tree.command(name="fruits", description="see all fruits name")
async def fruits(interaction: discord.Interaction):
    allF = ", ".join(all_fruits)
    await interaction.response.send_message(f"All fruits in the game is: \n{allF}")
@bot.tree.command(name="roll", description="roll a fruits")
@app_commands.checks.cooldown(1, 300, key=lambda i:(i.user.id))
async def roll(interaction: discord.Interaction):
    user_id = interaction.user.id
    cashs = money.get(user_id, 0)
    randomF = random.choices(all_fruits, weights=fruits_weight, k=1)[0]
    
    if user_id not in user_inventory:
        user_inventory[user_id] = []
        user_inventory[user_id].append(randomF)
    if user_id not in rolled:
        can_roll = True
    else:
        if cashs >= 100:
            can_roll = True
        else:
            can_roll = False
    if can_roll:
        await interaction.response.send_message(f"spinning...")
        await asyncio.sleep(2)
        await interaction.edit_original_response(content=f"You've rolled {randomF}")
    else:
        await interaction.response.send_message("You can't roll!")
@roll.error
async def roll_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await interaction.response.send_message(f"You need to wait for {error.retry_after:.2f} seconds!", ephemeral=True)
@bot.tree.command(name="inventory", description="show your inventory")
async def inventory(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_inventory:
        user_inv = user_inventory[user_id]
        inv = ", ".join(user_inv)
        await interaction.response.send_message(f"Your inventory:\n{inv}",ephemeral=True)
    else:
        await interaction.response.send_message("You didn't roll anything! Type /roll to roll")
        
@tasks.loop(hours=3)
async def stocks():
    global current_stock
    current_stock = random.sample(all_fruits, k=3)
@bot.tree.command(name="stock", description="show dealer stocks")
async def stock(interaction: discord.Interaction):
    fruits = "🍎\n".join([f.capitalize() for f in current_stock])
    await interaction.response.send_message(f"Blox fruits dealer stocks:\n{fruits}")
@bot.tree.command(name="sell", description="sell fruits")
@app_commands.describe(fruits="Please select a fruits")
async def sell(interaction: discord.Interaction, fruits:str):
    user_id = interaction.user.id
    inv = user_inventory[user_id]
    if fruits.lower() in inv:
        if user_id not in money:
            money[user_id] = 0
        inv.remove(fruits)
        price = fruit_prices.get(fruits)
        money[user_id] += price
        
        await interaction.response.send_message(f"Successfully sold fruits!")
    else:
        await interaction.response.send_message("You don't have this fruits!")
@bot.tree.command(name="cash", description="show your cash")
async def cash(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_inventory:
        cashs = money.get(user_id, 0)
        await interaction.response.send_message(cashs)
token = os.getenv("TOKEN")
bot.run(token)