""" Table lookup backends for podop
"""

import aiohttp
import logging


class UrlTable(object):
    """ Resolve an entry by querying a parametrized GET URL.
    """

    def __init__(self, url_pattern):
        """ url_pattern must contain a format ``{}`` so the key is injected in
        the url before the query, the ``§`` character will be replaced with
        ``{}`` for easier setup.
        """
        self.url_pattern = url_pattern.replace('§', '{}')

    async def get(self, key, ns=None):
        """ Get the given key in the provided namespace
        """
        if ns is not None:
            key += "/" + ns
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_pattern.format(key)) as request:
                if request.status == 200:
                    result = await request.json()
                    return result

    async def set(self, key, value, ns=None):
        """ Set a value for the given key in the provided namespace
        """
        if ns is not None:
            key += "/" + ns
        async with aiohttp.ClientSession() as session:
            await session.post(self.url_pattern.format(key), json=value)

    async def iter(self, cat):
        """ Iterate the given key (experimental)
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_pattern.format(cat)) as request:
                if request.status == 200:
                    result = await request.json()
                    return result
