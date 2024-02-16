import discord
import random
import os
import openai
from dotenv import load_dotenv
from discord.ext import tasks
from discord import Intents, Client, Message

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
KEY = os.getenv('API_KEY')

openai.api_key = KEY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Define the states for the bot
states = ['Sleeping', 'Eating', 'Esport', 'Deadge']

# Define the probabilities for each state
probabilities = [0.9, 0.0499995, 0.0499995, 0.000001]

# Initialize the current state
current_state = 'Sleeping'

def get_response(user_input:str) -> str:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    return response['choices'][0]['message']['content']

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intent were not enabled)')
        return
    
    if is_private:=user_message[0]=='?':
        user_message = user_message[1:]
    
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    change_status.start()

@tasks.loop(minutes=1)
async def change_status():
    global current_state

    # If the bot is dying, stop changing status
    if current_state == 'Dying':
        change_status.cancel()
        return

    # Choose the next state based on the probabilities
    current_state = random.choices(states, weights=probabilities, k=1)[0]

    # Update the bot's status
    await client.change_presence(activity=discord.Game(name=current_state))


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'{username} in {channel} said: {user_message}')
    await send_message(message, user_message)





client.run(token=TOKEN)