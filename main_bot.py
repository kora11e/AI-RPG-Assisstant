import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv, dotenv_values
import json, requests
import get_voice
from deploy import evaluate
from conversation_context_window import ContextWindow

context_window = ContextWindow()

load_dotenv()

vc_id = '1159082304573014116'

'''
class Client(commands.Bot):
    #old version of the code, left for potential future usage

    async def on_ready(self):
        #channel.send('Welcome! My name is Drakwyn, an AI companion in your adventure.')
        print(f'Logs on as {self.user}!')
        try:
            GUILD_ID = discord.Object(id=None)
            synced = await self.tree.sync()
            print(f'synced successfully to {GUILD_ID.id}')
        except Exception as e:
            print(f'An error has occured: {e}')
    
    #@client.event
    async def on_member_join(self, member):
        channel = client.get_channel(1343135608251613319)
        await channel.send(f'{member} has joined the server! Feel free to talk to anyone!')

    async def on_member_leave(self, member):
        return

    #use later
    async def on_question(self, message):
        client2 = OpenAI(
            api_key := os.getenv("GPT_API"))
        prompt = "Who created and owns OpenAI?"

        chat_completion = client2.chat.completions.create(messages=[{
            'role': 'user',
            'content': prompt 
        }],
        model='gpt-3.5-turbo'
        )

        print(chat_completion.choices[0].message.content)

    async def on_drakwyn_prompt(self, prompt):
         return
    '''

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot has synced')
    await bot.tree.sync()

#join voice chat
@bot.hybrid_command(name='join_voice_channel')
async def join_vc(interaction: commands.Context):
    if (interaction.author.voice.channel):
        channel = interaction.author.voice.channel
        await channel.connect()
        print('Success!')
        #the outside AI model function goes here
        #get_voice.capture_voice()
    else:
        interaction.send("Please join voice channel so that I can follow you. UwU", ephemeral=True)

#leave voice chat OK
@bot.hybrid_command(name='leave_voice_channel')
async def leave_vc(interaction: commands.Context):
    if interaction.author.voice.channel:  # Check if the bot is in a voice channel
        await interaction.voice_client.disconnect()
    else:
        await interaction.send("I'm not in a voice channel!", ephemeral=True)

#Poland command OK
@bot.hybrid_command(name='poland')
async def sayPoland(interaction: commands.Context):
    await interaction.send("I love Poland. It's the best country in the world! <3!")

"""
#length of prompt checker for length of context 
def len_prompt(interaction: commands.Context, len_prompt: str):
    n = len(len_prompt)
    if n > 63:
        interaction.send(f'Your prompt is too long. Maximum length is 64 characters.')
    elif n == 0:
        interaction.send(f'Your ptrompt is empty. Please provide a question.')
    else:
        interaction.send(f'Length of the prompt is {n}. Good job!')
"""
#information command
@bot.hybrid_command(name='info')
async def sayPoland(interaction: commands.Context):
    await interaction.send(f"I'm Drakwyn, an intelligent AI bot designed to help you with your roleplay! May the force be with you <3!")

#prompt the message
@bot.hybrid_command(name='prompt')
async def sayPrompt(interaction: commands.Context, text):
    text = str(text)
    temperature = str(temperature)
    context_window.add_user_message(str(text))
    n = evaluate(prime_str=text)
    await interaction.send(str(n))
    context_window.add_system_message(str(n))
    #save text to file

#run the fucking bot and don't crush this time
bot.run(f'{os.getenv("TOKEN")}')
