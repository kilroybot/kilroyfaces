from typing import AsyncIterator, Iterator, Optional, Tuple, Union

import tweepy
from kilroyshare import Face

from kilroyfaces.twitter.auth import Auth
from kilroyfaces.twitter.scoring import LikeScorer, TweetScorer
from kilroyfaces.twitter.scraping import FollowingScraper, TweetScraper
from kilroyfaces.twitter.utils import tweet


class TwitterFace(Face[str, str]):
    client: tweepy.Client = None

    def __init__(
        self,
        auth: Auth,
        scorer: TweetScorer = LikeScorer(),
        scraper: TweetScraper = FollowingScraper(),
    ) -> None:
        super().__init__()
        self.auth = auth
        self.scorer = scorer
        self.scraper = scraper

    async def init(self) -> None:
        self.client = tweepy.Client(
            consumer_key=self.auth.consumer_key,
            consumer_secret=self.auth.consumer_secret,
            access_token=self.auth.token,
            access_token_secret=self.auth.secret,
        )

    async def scrap(
        self, limit: Optional[int] = None
    ) -> Union[Iterator[Tuple[str, str]], AsyncIterator[Tuple[str, str]]]:
        return self.scraper.scrap(limit, self.client)

    async def post(self, data: str) -> str:
        return tweet(data, self.client)

    async def score(self, post_id: str) -> float:
        return self.scorer.score(post_id, self.client)
