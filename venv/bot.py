import os

import discord
import random
import json
from discord.ext import commands
from dotenv import load_dotenv

# get token from .env file
load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

# file input/output
file = open('trivia.txt', 'r')
lines = file.readlines()

# seed random
random.seed()

# save user data
class user:
    def __init__(self, name, score):
        self.name = name
        self.score = score


data = {}
data['users'] = []

#global variables
active_flag = False
guessed = []

bot = commands.Bot(command_prefix='!')

@bot.command()
async def trivia(ctx, *args):
    global active_flag
    active_flag = True

    global chosen
    chosen = lines[random.randint(0, len(lines) - 1)]
    chosen = chosen.split('%')

    global answers
    answers = []

    global guessed
    guessed = []

    for i in range(1, 5):
        answers.append(chosen[i])

    random.shuffle(answers)

    await ctx.channel.send('**' + chosen[0] + '**' + '\n- ' + answers[0] + '\n- ' +
                           answers[1] + '\n- ' + answers[2] + '\n- ' + answers[3])

@bot.listen()
async def on_message(message):
    global active_flag
    global guessed

    if message.author == bot.user:
        return
    if message.content.startswith("!trivia"):
        return
    if active_flag:
        if message.content.lower() == chosen[5].rstrip('\n'):
            if (guessed.count(message.author.name) == 0):
                active_flag = False
                guessed = []
                await message.channel.send(message.author.name + " is correct!")
            else:
                await message.channel.send("Sorry " + message.author.name + ", you have already guessed!")
        else:
            if(guessed.count(message.author.name) == 0):
                guessed.append(message.author.name)
                await message.channel.send("Sorry " + message.author.name + ", that is incorrect!")
            else:
                await message.channel.send("Sorry " + message.author.name + ", you have already guessed!")

bot.run(TOKEN)

#client = discord.Client()

#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')

#client.run(TOKEN)

