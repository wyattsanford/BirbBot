import logging
import sys
import traceback

import aiohttp
import pendulum
from discord.ext import commands
import discord
from cogs.utils import context
from cogs.utils.esi import ESI

try:
    import config
except ImportError:
    print("Config not found, have you copied over the example settings?")
    sys.exit(1)


description = """
Rooster knows all...
"""

log = logging.getLogger(__name__)

initial_cogs = (
    'cogs.eft',
    'cogs.who',
    'cogs.insurance',
    'cogs.killwatch',
    'cogs.market',
    'cogs.reminder',
    'cogs.time',
    'cogs.thera',
    'cogs.trivia',
    'cogs.weather',
)


class Rooster(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!', 
            description=description, 
            pm_help=None, 
            help_attrs=dict(hidden=True))

        self.client_id = config.client_id
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.esi = ESI()

        self.add_command(self.disable)
        self.add_command(self.enable)
        self.add_command(self.listcogs)
        self.add_command(self.uptime)
        self.add_command(self.join)

        for cog in initial_cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print('Failed to load cog {}'.format(cog), file=sys.stderr)
                traceback.print_exc()

    async def on_comand_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in Private Messages')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry, this command is disabled.')
        elif isinstance(error, commands.CommandInvokeError):
            print('In {}'.format(ctx.command.qualified_name), file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)

    async def on_ready(self):
        if not hasattr(self, 'currentuptime'):
            self.currentuptime = pendulum.now(tz='UTC')
            print('Ready')

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)

        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_resumed(self):
        print('Resumed...')

    def run(self):
        super().run(config.token, reconnect=True)

    @property
    def config(self):
        return __import__('config')

    @commands.command(hidden=True)
    @commands.has_role('Administrator')
    async def disable(self, ctx, cogname):
        """
        Allows an Admin to disable a module
        """
        self.unload_extension(cogname)
        await ctx.send('OK')

    @commands.command(hidden=True)
    @commands.has_role('Administrator')
    async def enable(self, ctx, cogname):
        """
        Allows an Admin to enable a module
        """
        self.load_extension(cogname)
        await ctx.send('OK')

    @commands.command(hidden=True)
    @commands.has_role('Administrator')
    async def listcogs(self, ctx):
        """
        Lists modules available
        """
        x = []
        for i in self.extensions:
            x.append(i)
        await ctx.send(x)

    @commands.command(hidden=True)
    async def uptime(self, ctx):
        """
        Returns the uptime
        """
        await ctx.send(pendulum.now(tz='UTC').diff_for_humans(self.currentuptime, absolute=True))

    @commands.command(hidden=True, aliases=['invite'])
    async def join(self, ctx):
        """Joins a server."""
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.external_emojis = True
        perms.send_messages = True
        perms.manage_roles = False
        perms.manage_channels = False
        perms.ban_members = False
        perms.kick_members = False
        perms.manage_messages = False
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        perms.add_reactions = True
        await ctx.send('<{}>'.format(
            discord.utils.oauth_url(self.client_id, perms)))
