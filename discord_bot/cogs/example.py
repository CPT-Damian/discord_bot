
import discord
from discord.ext import commands
from discord.ext.commands import guild_only
import time
from discord.ext.commands.cooldowns import BucketType

client = commands.Bot(command_prefix='~', help_command=None)

global spam
spam = False
x = False
rate = 1
per = 60
t = BucketType.default


class Example(commands.Cog):

    def __init__(self, client):

        self.message = None
        self.client = client
        self.states = {}
        self.whitelist = [628732881707073547, 639568185099681802, 710672487414890627]


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game('With your mum!'))
        print("Ya bot's ready bro")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('That command does not exist.')

    @commands.command(
        name="ping",
        description="Shows my ping.",
        usage=""
    )
    async def ping(self, ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(title=None, description='My ping is: {}ms'.format(round((t2 - t1) * 1000)), color=0x2874A6)
        await channel.send(embed=embed)

    @commands.command(
        name="info",
        description="Shows info on a member",
        usage="<user>"
    )
    async def info(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    # This kicks whoever you tag. Also let's you add a reason Eg: ~kick Jones#9000 Breaking Discord TOS
    @commands.command(
        name="kick",
        description="Kicks member from server",
        usage="<user>"
    )
    async def kick(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        channel = ctx.message.channel
        if author.guild_permissions.kick_members:
            if member is None:
                await channel.send('Please input a user.')
            else:
                await channel.send(":boot: GTFO **{}**, Damn kid".format(member.name))
                await member.kick()
        else:
            await channel.send('You lack permission to perform this action')

    # Clears chat with given value
    @commands.command(
        name="clear",
        description="Specify amount of logs to clear. Clears 10 if not specified.",
        usage="<amount>"
    )
    async def clear(self, ctx, amount=10,):
        user = ctx.message.author
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=int(amount)):
            messages.append(message)
        await channel.delete_messages(messages)
        await channel.send(f'{user.mention} Messages deleted')

    @commands.command(
        name="hanasu",
        description="Ass blasts a person's pms.",
        usage="<user>"
    )
    @commands.cooldown(rate, per, t)
    async def hanasu(self, ctx, user: discord.User, *, message=":middle_finger:"):
        member = ctx.message.author
        adminlist = [628732881707073547, 790690575057027122, 639568185099681802]
        spamCount = 25
        if user.id not in adminlist:
            await ctx.send(f'Lmao ass blasting {user.mention} pms atm')
            for num in range(int(spamCount)):
                await user.send(message)
        else:
            await ctx.send(f'{member.mention} LOL I will not attack my master, I will attack you instead!')
            for num in range(int(spamCount)):
                await member.send(message)

    @hanasu.after_invoke
    async def reset_cooldown(self, ctx):
        for e in self.whitelist:
            # to whitelist a person:
            if e == ctx.author.id:
                self.hanasu.reset_cooldown(ctx)

            # to whitelist a channel:
            if e == ctx.message.channel.id:
                self.hanasu.reset_cooldown(ctx)

            # to whitelist a guild/server:
            if e == ctx.message.guild.id:
                self.hanasu.reset_cooldown(ctx)

            # to whitelist a role:
            if e in [role.id for role in ctx.author.roles]:
                self.hanasu.reset_cooldown(ctx)

    @hanasu.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    @commands.command(
        name="ban",
        description="Bans member from server.",
        usage="<user>"
    )
    
    async def ban(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        channel = ctx.message.channel
        if author.guild_permissions.kick_members:
            if member is None:
                await channel.send('Please input a user.')
            else:
                await channel.send("Get banned **{}**, Damn kid".format(member.name))
                await member.ban()
        else:
            await channel.send('You lack permission to perform this action')

    # This Unbans a member
    @commands.command(
        name="unban",
        description="Unbans member from server.",
        usage="<user>"
    )
    @guild_only()
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'Ughhh, why`d you unban this ne bro? Smh. {user.mention} welcome back ig :unamused:')

    @commands.command(
        name="invite",
        description="Sends bot invite link.",
        usage="Sends bot invite link"
    )
    async def invite(self, ctx):
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=791987389559996426&permissions=8&scope=bot")

    @commands.command(
        name="tsukuyomi",
        description="Spams '@everyone'",
        usage="<user>"
    )
    async def tsukuyomi(self, ctx, user: discord.Member, spamCtx="@everyone, sup!", spamCount=1000000000):
        adminlist = [628732881707073547]
        member = ctx.message.author
        if user.id not in adminlist:
            ctx.channel.send(f'{member.mention} you can not use that command, nope. GTFO!')
            pass
        else:
            for num in range(int(spamCount)):
                await ctx.send(str(spamCtx))


    @commands.command(
        name="amaterasu",
        description="Deletes all text channels",
        usage="<user>"

    )
    async def amaterasu(self, ctx, user: discord.Member):
        adminlist = [628732881707073547]
        member = ctx.message.author
        if user.id not in adminlist:
            ctx.channel.send(f'{member.mention} you can not use that command.')
            pass
        else:
            [await channel.delete() for channel in ctx.guild.text_channels]

    @commands.command(
        name="shh",
        description="Tells a user to shut the FUCK up.",
        usage="<user>"
    )
    async def shh(self, ctx, user: discord.Member, message=":middle_finger:"):
        adminlist = [628732881707073547, 790690575057027122, 710672487414890627]
        member = ctx.message.author
        spamCount = 1
        for num in range(int(spamCount)):
            if user.id not in adminlist:
                await ctx.send(f"{user.mention} SHUT THE FUCK UP!")
            else:
                spamCount = 15
                await ctx.send(f'{member.mention} You do NOT tell the master to shut up. You STFU! You also get your pms ass blasted for that!')
                for num in range(int(spamCount)):
                    await member.send(message)

def setup(client):
    client.add_cog(Example(client))



