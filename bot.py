from discord.ext import commands
import uuid
import json
from discord.utils import get
import asyncio


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


@bot.event
async def on_ready():
    print("bot is ready")


@bot.event
async def on_member_join(member):
    context = database.open()
    code = str(uuid.uuid4())[:6]
    context['userdb'][code] = member.id
    database.dump(context)
    await member.send(context['one'])
    await member.send(context['two'])
    await member.send(f"{context['three']}\n\nType this command to verify: `!verify {code}`")


@bot.command()
async def verify(ctx, code):
    context = database.open()
    if code in context['userdb'].keys():
        await ctx.message.delete()
        if ctx.message.channel.id == context['channel']:
            role = get(ctx.guild.roles, id=context['role'])
            await ctx.message.author.add_roles(role)
            del context['userdb'][code]
            database.dump(context)
    else:
        await ctx.send("The code is incorrect")
        await ctx.message.delete()

if __name__ == '__main__':
    context = database.open()
    bot.run(context['token'])

