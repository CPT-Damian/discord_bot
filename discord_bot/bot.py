
import os
from discord.ext import commands

client = commands.Bot(command_prefix='~', help_command=None)



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    ctx.send('Extension loaded.')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    ctx.send('Extension unloaded.')

cwd = "PATH/TO/FILE/DIRECTORY"
cwd = str(cwd)
print(cwd)

if __name__ == '__main__':
    for file in os.listdir(cwd + '/cogs'):
        if file.endswith('.py') and not file.startswith('_'):
            client.load_extension(f"cogs.{file[:-3]}")


client.run('My_Token')
