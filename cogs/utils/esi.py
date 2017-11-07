import json

import esipy
from esipy.cache import RedisCache
from discord.ext import commands
import redis

import config


class ESI:
    def __init__(self):
        #self.cache = FileCache(path='./esicache/')
        self.redis_client = redis.Redis(host='localhost', port=6379, db=1)
        self.cache = RedisCache(self.redis_client)
        self.esi_app = esipy.App.create(url='https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')
        self.esi_client = esipy.EsiClient(
            headers={'User-Agent': config.email},
            raw_body_only=True,
            cache=self.cache
        )

    def search(self, scope, entity):
        entity_search_operation = self.esi_app.op['get_search'](
            categories=[scope],
            search=entity,
            strict=True)
        response = self.esi_client.request(entity_search_operation)
        if not response:
            raise commands.BadArgument('ESI seems to be having a hard time, please try again later.')
        if scope not in self.jsonify(response.raw):
            raise commands.BadArgument('{} not found'.format(scope))
        else:
            return response

    def jsonify(self, raw):
        return json.loads(raw.decode('utf-8'))
