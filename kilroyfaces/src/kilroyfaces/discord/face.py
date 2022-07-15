from typing import AsyncIterator, Iterator, Optional, Tuple, Union

import discord
from discord import Message
from kilroyshare import Face

from kilroyfaces.discord.auth import Auth
from kilroyfaces.discord.scoring import MessageScorer, ReactionsScorer
from kilroyfaces.discord.scraping import ChannelScraper, MessageScraper


class DiscordFace(Face[int, str]):
    client: discord.Client = None
    channel = None

    def __init__(
        self,
        channel_id: int,
        auth: Auth,
        scorer: MessageScorer = ReactionsScorer(),
        scraper: Optional[MessageScraper] = None,
    ) -> None:
        super().__init__()
        self.channel_id = channel_id
        self.auth = auth
        self.scorer = scorer
        self.scraper = scraper or ChannelScraper(channel_id)

    async def init(self) -> None:
        self.client = discord.Client()
        await self.client.login(self.auth.token)
        self.channel = await self.client.fetch_channel(self.channel_id)

    async def cleanup(self) -> None:
        await self.client.close()

    async def scrap(
        self, limit: Optional[int] = None
    ) -> Union[Iterator[Tuple[int, str]], AsyncIterator[Tuple[int, str]]]:
        async for message in self.scraper.scrap(limit, self.client):
            yield message

    async def post(self, data: str) -> int:
        message: Message = await self.channel.send(data)
        return message.id

    async def score(self, post_id: int) -> float:
        return await self.scorer.score(self.channel, post_id)
