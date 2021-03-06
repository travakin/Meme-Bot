
import os
from CustomClient import CustomClient
import ReactValues
import discord
import datetime
from dotenv import load_dotenv

def get_points_per_member(members_dict, member_messages):
    for member in members_dict:
        members_dict[member] = get_points(member_messages[member])

def get_all_member_messages(guild, members, messages):
    #This function will grab all messages from TODAY
    #to back SEVEN days ago
    #list of members/messages - FORMAT = {member_name : [messages]}
    member_messages = {}
    for member in members:
        member_messages[member] = []
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)

    #GET_ALL_MESSAGES
    for message in messages:
        if message.created_at > week_ago and len(message.attachments) > 0:
            member_messages[message.author].append(message)

    return member_messages

def get_points(messages):

    points = 0

    for message in messages:
        for react in message.reactions:

            react_count = react.count

            if(react in ReactValues.reacts):
                points += ReactValues.reacts[react] * react_count
            else:
                points += ReactValues.default_value * react_count

    return points

def shame_and_glory(bot_channel, members_dict):

    top3 = members_dict[0:3]
    shame_list = []
    shame_message = "~~ATTENTION!!!~~\n"

    for member in members_dict:
        if member[1] == 0:
            shame_list.append(member)

    #print(top3[0])
    #Get rid of King Meme Ladicus - He cannot have shame for he is a KING
    #Also there's probably a better way to do this
    for member in shame_list:
        if str(member[0]) == "King Meme Ladicus the 69th#2451":
            shame_list.remove(member)

    glory_message1 = "1. " + (top3[0][0].nick or top3[0][0].name)
    glory_message2 = "2. " + (top3[1][0].nick or top3[1][0].name)
    glory_message3 = "3. " + (top3[2][0].nick or top3[2][0].name)

    for member in shame_list:
        try:
            shame_message += member[0].nick + "\n "
        except:
            shame_message += str(member[0]) + "\n "
            

    shame_message += "These FOOLS have not received a SINGLE meme like and should be SHAMED. DO BETTER THIS WEEK.\n"

    return glory_message1, glory_message2, glory_message3, shame_message

