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

    def to_dict(self):
        return {'name': self.name, 'score': self.score}

    def dump(self):
        return {"user": {'name': self.name, 'score': self.score}}

user_data = []

with open('user_data.json', 'r') as f:
    data = json.loads(json.load(f))

    for dictionary in data:
        user_data.append(user(dictionary['name'], dictionary['score']))

f.close()

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

    #random.shuffle(answers)

    await ctx.channel.send('>>> **' + chosen[0] + '**' + '\na. ' + answers[0] + '\nb. ' +
                           answers[1] + '\nc. ' + answers[2] + '\nd. ' + answers[3])

@bot.command()
async def score(ctx, args):
    global user_data
    global user

    for user in user_data:
        if user.name == args:
            await ctx.channel.send('>>> ' + user.name + '\'s score: ' + '**' + str(user.score) + '**')

@bot.listen()
async def on_message(message):
    global active_flag
    global guessed
    global user_data
    global user

    flag = True

    if message.author == bot.user:
        return
    if message.content.startswith("!"):
        return
    if active_flag:
        if message.content.lower() == chosen[5].rstrip('\n'):
            if (guessed.count(message.author.name) == 0):
                active_flag = False
                guessed = []

                # save user points
                for user in user_data:
                    if message.author.name == user.name:
                        user.score += 1
                        flag = False

                if flag:
                    user_data.append(user(message.author.name, 1))

                with open('user_data.json', 'w') as f:
                    user_json = [user.to_dict() for user in user_data]
                    json_data = json.dumps(user_json)
                    json.dump(json_data, f)

                f.close()

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

