import logging
import sys
import traceback
import aiohttp
import asyncio
# import pendulum
import discord
from discord.ext import commands
#import aioredis


try:
	import config #config contains token client id, API, and other method settings
except ImportError:
	print("Config not found, have you copied over the example settings?")
	sys.exit(1)

description = '''Birbbot v 1.0'''
#command_prefix='b.'
#bot = commands.Bot(command_prefix, description)

print(sys.version)

initial_feathers = (
#	'feathers.eft',
#	'feathers.who',
#	'feathers.insurance',
#	'feathers.killwatch',
#	'feathers.market',
#	'feathers.remind',
	'feathers.timeComp',
#	'feathers.thera',
#	'feathers.trivia',
#	'feathers.weather',
	'feathers.time',
)

print(discord.__version__)

class Birbbot(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix='b.',
			description=description,
			pm_help=None,
			help_attrs=dict(hidden=True))

		self.client_id = config.client_id

		self.session = aiohttp.ClientSession(loop=self.loop)
		self.esi = ESI ()

		self.add_command(self.uptime)
		self.add_comand(self.join)

	async def start_redis(self):
		self.redis = await aioredis.create_pool(
			('localhost', 6379), minsize=5, maxsize=10)

	async def on_ready(self):
		await self.start_redis()
#		self.currentuptime = pendulum.now(tz='UTC')
		print('Logged in as')
		print('------')
		print('Ready')

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=context.Context)

		if ctx.command is None:
			return
		await self.invoke(ctx)

	def run(self):
		super().run(config.TOKEN, reconnect=True)

	@property
	def config(self):
		return __import__('config')

	@commands.command(hidden=True, aliases=['invite']
	async def join(*args, **kwargs):
                """Joins a server."""
                perms = discord.Permissions.none()
                perms.read_messages = True
                perms.external_emojis = True
                perms.send_messages = True
                perms.manage_roles = False
                perms.manage_channels = False
                perms.ban_members = False
                perms.kick_members = False
                perms.embed_links = True
                perms.read_message_history = True
                perms.attach_files = True
                perms.add_reactions = True
                await ctx.send('<{}>'.format(
                        discord.utils.oath_url(self.client_id, perms)))

#bot.run('Mzc3MTUzNzc2MzYyMDYxODQ4.DOJDFg.hfYkAOBifDsOj5ewuNY1hJcUd7k')
