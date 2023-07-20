# This example requires the 'message_content' intent.
from dotenv import load_dotenv
import openai
import discord
from discord import app_commands
from discord.ext import commands
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="ai", description="ask chatgpt anything")
async def ai(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    response = chatgpt_response(message)
    await interaction.followup.send(content=f"User input: {message.strip()}\n\nAI Response: {response.strip()}")

def chatgpt_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    ) 
    response_dict = response.get("choices")
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]["text"]
    return prompt_response

bot.run(TOKEN)

#@tree.command(name="name", description="description")
#async def slash_command(interaction: discord.Interaction):    
#    await interaction.response.send_message("command")

#class MyClient(discord.Client):
#    async def on_message(self, message):
#        print(message.content)
#        if message.author == self.user:
#            return
#        command, user_message=None, None

#        for text in ['/ai', '/bot', '/chatgpt']: 
#            if message.content.startswith(text):
#                command=message.content.split(' ')[0]
#                user_message=message.content.replace(text,'')
#                print(command, user_message)
        #if command == '/ai' or command == '/bot' or command == '/chatgpt':
        #    bot_response = chatgpt_response(prompt=user_message)
        #    await message.channel.send(f"Answer: {bot_response}")
