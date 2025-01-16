''' SRBot

Using guide https://realpython.com/how-to-make-a-discord-bot-python/#welcoming-new-members
Discord API docs https://discordpy.readthedocs.io/en/stable/api.html
Context documentation https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context

Using the bot commands method of creating a bot
Relevant documentation https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#
Registering the bot. This lets us use the @bot decorator instead of creating a whole new bot
'''

# Standard libraries
from json import loads
from pathlib import Path
from typing import Literal, Optional

# Local environment
from SRBot.SRB.SRB import SRB

# PyPi Libraries
import discord
from discord.ext import commands
from dotenv import dotenv_values

# Loading settigs from config file
with open(Path().resolve() / 'config.json', mode='r', encoding='utf-8') as config_file:
    CONFIG = loads(config_file.read())


bot = discord.Bot()


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


@bot.slash_command(description='Add someone as a recruit')
@commands.has_any_role(*CONFIG['auth_roles']['recruiter'])
async def recruit(ctx, member: discord.Member, name: str=None):
    await member.add_roles(ctx.guild.get_role(CONFIG['role_assignments']['recruit']), reason=f'{ctx.author.name} recruited {member.name}')

    # Setting new name
    new_name = name or member.nick
    new_nick = new_name if new_name.startswith('[RCT]') else f'[RCT] {new_name}'
    await member.edit(nick = f'{new_nick}')

    # Telling our caller that the opertion was succesfull
    await ctx.respond(f'{new_name} as been recruited!', ephemeral=True)


@bot.slash_command(description='Used to quickly discharge a user using their user id')
@commands.has_any_role(*CONFIG['auth_roles']['s1'])
async def discharge(ctx, member: discord.Member, kick: bool=False):
    # Getting our default role and it's position
    default_role = ctx.guild.get_role(CONFIG['role_assignments']['default'])
    default_role_position = default_role.position

    # Removing all roles above the default role, then adding our default role
    await member.remove_roles(
        *[role for role in member.roles if role.position > default_role_position]
    )
    await member.add_roles(default_role)

    # Resetting the members nickname
    old_nick = member.nick
    await member.edit(nick='')

    # Notifying our caller
    await ctx.respond(f'{old_nick} has been discharged from the unit.')


@bot.slash_command(description='Used to view SRB information given a discord ID or DODID')
@commands.has_any_role(CONFIG['role_assignments']['member'])
async def member(ctx, member: discord.Member=None, dodid: str=None):
    if member:
        member = SRB().get_member(discord_id = member.id)
    elif dodid:
        member = SRB().get_member(dodid = dodid)
    else:
        embed = discord.Embed(
            title='SRB Command Error:',
            description='Must provide an argument to either dodid or discord member parameter.',
            color=discord.Colour.red(),
        )
        await ctx.respond('', ephemeral=True, embed=embed)
        return
    await ctx.respond(f'```{member.to_string(index=False)}```')


bot.run(dotenv_values('.env')['DISCORD_TOKEN'])
