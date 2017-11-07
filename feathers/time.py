import asyncio
import logging

import dateparser
import pendulum
from discord.ext import commands

from discord import embeds

log = logging.getLogger(__name__)


class Time:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def time(self, ctx):
        """
        Get current eve time - !help time for more options
        """
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                await asyncio.sleep(.5)
                return await ctx.send(embed=embeds.Embed(title='Current Eve Time:',
                                                         description=pendulum.utcnow().to_datetime_string()))

    @time.command()
    async def until(self, ctx, *, time):
        """
        Attempts to tell you how long until <time> in EVE time.
        """
        async with ctx.typing():
            await asyncio.sleep(.5)

            parsedtime = dateparser.parse(time, settings={'TIMEZONE': 'UTC', 'PREFER_DATES_FROM': 'future'})
            if not parsedtime:
                raise commands.BadArgument('Sorry, I cannot process that time argument')
            now = pendulum.now(tz='UTC')

            # dateparser can struggle with some human terms like 3 hours vs in 3 hours, so we force literally everything
            # to be parsed as the future.  it's a dum hack and I'd like to improve this
            if parsedtime < now:
                future = now - parsedtime
                parsedtime = now + future + future

            timediff = embeds.Embed()

            timediff.add_field(name='Current EVE Time:', value=now.to_datetime_string(), inline=False)
            timediff.add_field(name='Interpreted Time:', value=parsedtime, inline=False)
            timediff.add_field(name='Time Until:', value=parsedtime-now, inline=False)

            return await ctx.send(embed=timediff)

    @time.command()
    async def add(self, ctx, *, time):
        """
        Adds <time> to the current eve time
        """
        async with ctx.typing():
            await asyncio.sleep(.5)
            parsedtime = dateparser.parse(time, settings={'TIMEZONE': 'UTC', 'PREFER_DATES_FROM': 'future'})
            if not parsedtime:
                raise commands.BadArgument('Sorry, I cannot process that time argument')

            now = pendulum.now(tz='UTC')
            newtime = now + now.diff(parsedtime)

            timeadd = embeds.Embed()
            timeadd.add_field(name='Current EVE Time:', value=pendulum.now(tz='UTC').to_datetime_string(),
                              inline=False)
            timeadd.add_field(name='New EVE Time:', value=newtime.to_datetime_string(), inline=False)

            return await ctx.send(embed=timeadd)

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        else:
            await ctx.send('An error occurred, this has been logged')
            log.warning(error)
            log.warning(ctx.message.content)


def setup(bot):
    bot.add_cog(Time(bot))
