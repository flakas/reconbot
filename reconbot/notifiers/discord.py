import discord
import asyncio

class DiscordNotifier:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.client = discord.Client()

    def notify(self, text, options={}):
        if 'channel' in options:
            channel_id = options['channel_id']
        else:
            channel_id = self.channel_id

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._send_message(channel_id, text))

    async def _send_message(self, channel_id, message):
        await self.client.login(self.token)
        self.client.connect()
        c = discord.Object(id=channel_id)
        await self.client.send_message(c, message)
        await self.client.logout()
        await self.client.close()
