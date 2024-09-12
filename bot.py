import discord
from discord.ext import tasks
import os
import dotenv
import random
import glob
import sys
try:
    sys.path.insert(1, 'C:\\Dev\\LightDiffusion\\')
    from LightDiffusion import pipeline
except: print("LightDiffusion not available or incorrectly accessed, proceeding without generative AI")

dotenv.load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

states = ['Sleeping', 'Eating', 'Esport', 'Deadge']
probabilities = [0.8, 0.0999995, 0.0999995, 0.000001]
current_state = 'Waking up'

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
@tasks.loop(minutes=1)
async def change_status():
    global current_state
    if current_state == 'Dying':
        change_status.cancel()
        return
    current_state = random.choices(states, weights=probabilities, k=1)[0]
    await bot.change_presence(activity=discord.Game(name=current_state))

@bot.command()
async def generate(ctx, prompt: discord.Option(str), width: discord.Option(int), height: discord.Option(int)):
    await ctx.respond(f"here's a picture of : {prompt}")
    pipeline(prompt, width, height)
    image_files = glob.glob('C:\\Dev\\LightDiffusion\\_internal\\output\\*.png')
    print(max(image_files, key=os.path.getctime))
    await ctx.followup.send(file=discord.File(max(image_files, key=os.path.getctime)))

@bot.command()
async def hello(ctx):
  await ctx.respond(f"Hello, {ctx.author}!")

bot.run(TOKEN)