import discord
from discord.ext import commands
import uuid
import json
from discord.utils import get
import asyncio

# Warning logging to the console
import logging

logging.basicConfig(level=logging.WARNING)

# Discord Intents
intents = discord.Intents.default()
intents.members = True

class DbHandler:
    def __init__(self, file):
        self.file = file

    def dump(self, context):
        with open(self.file, 'w') as w:
            json.dump(context, w, indent=2)

    def open(self):
        with open(self.file) as r:
            return json.load(r)


bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), case_insensitive=True)
database = DbHandler('settings.json')

# Prints to console when bot is loaded and ready to handle users
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the gate"))
    print("Bot has Loaded")

# Event that triggers when someone joins the server
@bot.event
async def on_member_join(member):
    context = database.open()
    code = str(uuid.uuid4())[:6]
    context['userdb'][code] = member.id
    database.dump(context)
    channel = bot.get_channel (context['channel'])
    await channel.send(f"**Welcome to the server **{member.mention} \n\n I sent you a **Private Message,** Please read it. It contains the rules that you need to know and a secret command. After you read the rules paste that command in **this** channel. Breaking certian rules gives you a permanent ban with no warning.")
    await member.send(context['one'])
    await member.send(context['two'])
    await member.send(f"{context['three']}\n\nCopy Paste this command in #welcome to verify:")
    await member.send(f"!verify {code}")
    

# Event for when someone enters their verification code
@bot.command()
async def verify(ctx, code):
    context = database.open()
    if code in context['userdb'].keys():
        if ctx.message.channel.id == context['channel']:
            role = get(ctx.guild.roles, id=context['role'])
            await ctx.message.author.add_roles(role)
            await ctx.send(ctx.author.mention+" is human and has accepted the rules.")
            del context['userdb'][code]
            database.dump(context)
            await ctx.message.delete()

    else:
        await ctx.send("You have entered an incorrect code, Please check again or send a PM to Modmail")
        await ctx.message.delete()
        

if __name__ == '__main__':
    context = database.open()
    bot.run(context['token'])

