import discord
from discord.ext import commands
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

user_times = {}
tz = pytz.timezone('Europe/Sarajevo')

def get_day_name(date):
    days = {
        0: "Ponedjeljak",
        1: "Utorak",
        2: "Srijeda",
        3: "Četvrtak",
        4: "Petak",
        5: "Subota",
        6: "Nedjelja"
    }
    return days[date.weekday()]

@bot.event
async def on_ready():
    print(f'{bot.user} je online!')
    try:
        synced = await bot.tree.sync()
        print(f'Sinhronizovano {len(synced)} komandi')
    except Exception as e:
        print(e)

@bot.tree.command(name="start", description="Započni računanje radnog vremena")
async def start(interaction: discord.Interaction):
    user_id = interaction.user.id
    current_time = datetime.now(tz)
    user_times[user_id] = current_time
    vrijeme = current_time.strftime("%H:%M")
    datum = current_time.strftime("%d.%m.%Y")
    dan = get_day_name(current_time)
    
    await interaction.response.send_message(
        f"✅ Započeli ste računanje radnog vremena u **{vrijeme}**, {datum} ({dan})"
    )

@bot.tree.command(name="stop", description="Zaustavi računanje radnog vremena")
async def stop(interaction: discord.Interaction):
    user_id = interaction.user.id
    
    if user_id not in user_times:
        await interaction.response.send_message(
            "❌ Trebate prvo pokrenuti `/start` komandu!"
        )
        return
    
    start_time = user_times[user_id]
    stop_time = datetime.now(tz)
    elapsed = stop_time - start_time
    hours = elapsed.seconds // 3600
    minutes = (elapsed.seconds % 3600) // 60
    
    vrijeme = stop_time.strftime("%H:%M")
    datum = stop_time.strftime("%d.%m.%Y")
    dan = get_day_name(stop_time)
    
    if hours > 0:
        work_time = f"{hours}h {minutes}min"
    else:
        work_time = f"{minutes}min"
    
    await interaction.response.send_message(
        f"🛑 Zaustavili ste u **{vrijeme}**, {datum} ({dan})\n"
        f"📊 Radili ste: **{work_time}**"
    )
    
    del user_times[user_id]

bot.run(TOKEN)