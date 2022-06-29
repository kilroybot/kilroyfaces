from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional, Tuple

import discord
from discord.abc import Messageable


class MessageScraper(ABC):
    @abstractmethod
    async def scrap(
        self, limit: Optional[int], client: discord.Client
    ) -> AsyncIterator[Tuple[int, str]]:
        pass


class ChannelScraper(MessageScraper):
    def __init__(self, channel_id: int) -> None:
        super().__init__()
        self.channel_id = channel_id

    async def scrap(
        self, limit: Optional[int], client: discord.Client
    ) -> AsyncIterator[Tuple[int, str]]:
        channel: Messageable = await client.fetch_channel(self.channel_id)
        async for message in channel.history(limit=limit):
            yield message.id, message.content
