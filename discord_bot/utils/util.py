import asyncio
import discord
from discord.ext.buttons import Paginator


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


async def GetMessage(
        bot, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100
):
    embed = discord.Embed(
        title=f"{contentOne}",
        description=f"{contentTwo}",
    )
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel,
        )
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False