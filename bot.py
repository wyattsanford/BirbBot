import logging
import sys
import traceback

import aiohttp
import pendulum
from discord.ext import commands
import discord

try:
	import config #config contains token client id, API, and other method settings
except ImportError:
	print("Config not found, have you copied over the example settings?")
	sys.exit(1)

description = '''Birbbot v 1.0'''


initial_feathers = (
#	'feathers.eft',
	'feathers.who',
#	'feathers.insurance',
#	'feathers.killwatch',
	'feathers.market',
#	'feathers.remind',
#	'feathers.timeComp',
#	'feathers.thera',
#	'feathers.trivia',
	'feathers.weather',
)

class Birbbot(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix='b.',
			description=description,
			pm_help=None,
			help_attrs=dict(hidden=True))

	async def start_redis(self):
		self.redis = await aioredis.create_pool(
			('localhost', 6379), loop=self.loop)

	async def on_ready(self):
		if not hasattr(self, 'currentuptime'):
			await self.start_redis()
			self.currentuptime = pendulum.now(tz='UTC')
		print('Logged in as')
		print(bot.user.name)
		print('------')
		print('Ready')
