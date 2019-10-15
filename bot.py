import discord
import random, os
import subprocess

from asyncio import sleep
from discord.ext import commands

# User loads their laundry first, then washes and dries it
# After drying, they should be billed a lot of money

prefix = '.'
client = commands.Bot(command_prefix = prefix)

@client.event
async def on_ready():
      print('Laundry Services bot is ready.')


class Status:
    def __init__(self, dry_occupied, wash_user, dry_user):
        self.dry_occupied = dry_occupied
        self.wash_user = wash_user
        self.dry_user = dry_user

# Preset status to all machines unoccupied
status = Status(False, None, None)


# Load laundry
@client.command()
async def load(ctx):

    # If washing machine not occupied, author of command is wash_user
    if status.wash_user == None:
        status.wash_user = ctx.author
        await ctx.send(f'@{status.wash_user}, your laundry has been loaded. Use .wash to wash it.')

    # If washing machine occupied, notify user
    else:
        await ctx.send(f'The machine is currently full with {status.wash_user}\'s laundry.')

    print(status.wash_user)


# Wash laundry 
@client.command()
async def wash(ctx):

    # If the author of command is the same person who loaded the washing machine, ...
    if ctx.author == status.wash_user:    
        await ctx.send('Starting wash cycle, please wait 30 seconds ...')
        await sleep(30)
        await ctx.send(f'@{status.wash_user}, your laundry has been washed. Use .dry to dry it.')

        # Grant access for washing machine
        status.dry_user = status.wash_user

    # If the washing machine is empty, prompt user to use load command first
    elif status.wash_user == None:
        await ctx.send('You must load your clothes into the machine first!')
        
    # Someone else is using the machine
    else:
        await ctx.send(f'{status.wash_user}\'s wash cycle in progress, please wait...')


# Dry laundry
@client.command()
async def dry(ctx):

    # If the author of the command has been granted access to the dryer
    if ctx.author == status.dry_user:

        # If the dryer is not already occupied, it is now. Washing machine gets free'd up.
        if not status.dry_occupied:
            status.dry_occupied = True
            status.wash_user = None

            await ctx.send('Starting dry cycle, please wait 30 seconds...')
            await sleep(30)
            await ctx.send(f'@{status.dry_user}, your laundry has been dried.')

            total = random.randint(100, 15000)
            await ctx.send(f'Your total is ${total}')

            # Drying is done so dryer is now unoccupied.
            status.dry_occupied = False
            status.dry_user = None

        # Someone else is using the dryer
        else:
            await ctx.send(f'{status.dry_user}\'s dry cycle in progress, please wait...')

    # If the user hasn't washed their clothes, prompt them to do so
    elif ctx.author != status.dry_user:
        await ctx.send('You must wash your clothes before drying them!')

    else:
        pass


# Checks if user is an administrator
def is_admin(user): 
    return user.guild_permissions.administrator


# Calls git commands from terminal
def git(*args):
    return subprocess.check_call(['git'])


# Restarts the bot
@commands.command()
async def reset(ctx):

    logger("reset", ctx, True)
    
    if is_admin(ctx.message.author):
        await ctx.send('Restarting Laundry Bot...')
        git("clone", "https://github.com/helloMusa/Laundry-Bot") # Clones repo
        os.execv('/home/ubuntu/laundry_services_bot/Laundry-Bot/bot.py', sys.argv) # Restart the bot

    else:
        await ctx.send('You are not authorized to use this command.')

    logger("reset", ctx, False)


def main():

    client.add_command(load)
    client.add_command(wash)
    client.add_command(dry)
    client.add_command(admin)

     if len(sys.argv) < 2:
        print(f'ERROR 0: No Client Token Provided')
        sys.exit

    bot_token = sys.argv[1]
    client.run(bot_token)


if __name__ == '__main__':
    main()