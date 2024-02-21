import discord
import os
import dotenv
import random
from discord.ext import tasks
import workflow_api
import glob

dotenv.load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

states = ['Sleeping', 'Eating', 'Esport', 'Deadge']
probabilities = [0.8, 0.0999995, 0.0999995, 0.000001]
current_state = 'Waking up'

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    change_status.start()

@tasks.loop(minutes=1)
async def change_status():
    global current_state
    if current_state == 'Dying':
        change_status.cancel()
        return
    current_state = random.choices(states, weights=probabilities, k=1)[0]
    await bot.change_presence(activity=discord.Game(name=current_state))

@bot.command()
async def generate(ctx, phrase: discord.Option(str), adjectives: discord.Option(str)):
    await ctx.respond(f"here's a picture of : {phrase} \n whith : {adjectives}")
    workflow_api.gen(phrase, adjectives)
    #open the last image in /output and send it
    image_files = glob.glob('C:/Users/Aatricks/Desktop/ComfyUI/output/*.png')
    latest_image = max(image_files, key=os.path.getctime)
    await ctx.send(file=discord.File(latest_image))

bot.run(TOKEN)