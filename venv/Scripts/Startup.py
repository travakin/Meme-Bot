import os
from CustomClient import CustomClient
import ReactValues
import discord
import datetime
from MemerOfTheWeek import get_points_per_member, get_all_member_messages, shame_and_glory
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('MEMER_CHANNEL')
GLORY_HEADER = os.getenv('GLORY_HEADER')
GLORY_TITLE = os.getenv('GLORY_TITLE')
GLORY_FOOTER = os.getenv('GLORY_FOOTER')

client = CustomClient()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    for channel in guild.text_channels:
        if(channel.name == CHANNEL):
            bot_channel = channel
            break

    members = [member for member in guild.members]
    members_dict = {}

    for member in members:
        members_dict[member] = 0

    messages = []

    for channel in guild.text_channels:
        async for message in channel.history(limit=100000):
            messages.append(message)

    member_messages = get_all_member_messages(guild, members, messages)

    get_points_per_member(members_dict, member_messages)
    members_dict = sorted(members_dict.items(), key=lambda x:x[1], reverse=True)

    glory_msg1, glory_msg2, glory_msg3, shame_msg = shame_and_glory(bot_channel, members_dict)

    print(glory_msg1)
    print(glory_msg2)
    print(glory_msg3)

    await bot_channel.send(GLORY_HEADER)
    await bot_channel.send(GLORY_TITLE + " " + datetime.datetime.today().strftime('(%d %b, %Y)'))
    await bot_channel.send(glory_msg1)
    await bot_channel.send(glory_msg2)
    await bot_channel.send(glory_msg3)
    await bot_channel.send(GLORY_FOOTER)

client.run(TOKEN)

