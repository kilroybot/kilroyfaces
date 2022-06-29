from abc import ABC, abstractmethod

from discord import Message
from discord.abc import Messageable


class MessageScorer(ABC):
    @abstractmethod
    async def score(self, channel: Messageable, message_id: int) -> float:
        pass


class ReactionsScorer(MessageScorer):
    async def score(self, channel: Messageable, message_id: int) -> float:
        message: Message = await channel.fetch_message(message_id)
        return sum(reaction.count for reaction in message.reactions)
