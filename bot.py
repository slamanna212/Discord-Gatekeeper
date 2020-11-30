import discord
from discord.ext import commands
from discord.utils import get
import uuid
import json
import logging

logging.basicConfig(level=logging.WARNING)


"""  # I rather save to file using the default discord config.
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
"""

# Discord Intents
intents = discord.Intents(messages=True, guilds=True, members=True)

class DbHandler:
    def __init__(self, file):
        self.file = file

    def dump(self, context):
        with open(self.file, 'w') as w:
            json.dump(context, w, indent=2)

    def open(self):  # I suggest renaming this method to "load".
        with open(self.file) as r:
            return json.load(r)


database = DbHandler('settings.json')

# Added global variables for dryness
DB = database.open()
VERIFICATION_CHANNEL = DB['channel']
TOKEN = DB['token']
ROLE_ID = DB['role']

bot = commands.Bot(command_prefix=commands.when_mentioned_or('! ', '!'),  # On mobile autocorrect sometimes adds a space after the prefix. This way commands get recognized regardless
                   case_insensitive=True,
                   intents=intents)


# Prints to console when bot is loaded and ready to handle users
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the gate"))
    print("Bot has Loaded")


# Event that triggers when someone joins the server
@bot.event
async def on_member_join(member):
    db = database.open()
    code = str(uuid.uuid4())[:6]  # Just know this basically defeats the purpose of uuid and might run into collisions
    while code in db['userdb'].keys(): # This would prevent overriding a code if somehow it got duplicated
        code = str(uuid.uuid4())[:6]
    db['userdb'][code] = member.id
    database.dump(db)
    channel = bot.get_channel(VERIFICATION_CHANNEL)
    await channel.send(f"**Welcome to the server **{member.mention} \n\n I sent you a **Private Message,** Please read it. It contains the rules that you need to know and a secret command. After you read the rules paste that command in **this** channel. Breaking certian rules gives you a permanent ban with no warning.")
    await member.send(db['msg']['one'])  # added msg just for readability
    await member.send(db['msg']['two'])
    await member.send(f"{db['msg']['three']}\n\nCopy Paste this command in <#{VERIFICATION_CHANNEL}> to verify:")  # might as well just add a shortcut.
    await member.send(f"!verify {code}")



# Command for users to verify themselves with the code they got when joining the server
@bot.command()
async def verify(ctx, code):
    await ctx.message.delete()  # moved here because you're going to delete it anyways and keeps it dry.
    if ctx.message.channel.id != VERIFICATION_CHANNEL:
        await ctx.send(f'This command can only be run in <#{VERIFICATION_CHANNEL}>', delete_after=5.0)  #  points the user to the right direction, but prevents clutter
        return
    db = database.open()  # Edited variable name because the command already has a "ctx" variable which is in fact a "context".
    if code in db['userdb'].keys() and ctx.author.id == db['userdb'][code]:  # i mean, you might as well check its the correct code for the user.
        del db['userdb'][code]
        database.dump(db)

        role = get(ctx.guild.roles, id=ROLE_ID)
        await ctx.message.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is human and has accepted the rules.")
    elif ctx.author.id in db['userdb'].values():
        await ctx.send("You have entered an incorrect code, Please check again or send a PM to Modmail")
    else:
        ctx.send('You were verified before, no need to run the verification command again.')


if __name__ == '__main__':
    bot.run(TOKEN)

