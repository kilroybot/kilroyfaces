from typing import Iterator, Optional, Tuple

import tweepy
from kilroyshare import Face

from kilroyfaces.twitter.auth import Auth
from kilroyfaces.twitter.scoring import LikeScorer, TweetScorer
from kilroyfaces.twitter.scraping import FollowingScraper, TweetScraper
from kilroyfaces.twitter.utils import tweet


class TwitterFace(Face[str, str]):
    def __init__(
        self,
        auth: Auth,
        scorer: TweetScorer = LikeScorer(),
        scraper: TweetScraper = FollowingScraper(),
    ) -> None:
        super().__init__()
        self.scorer = scorer
        self.scraper = scraper
        self.client = self.build_client(auth)

    @staticmethod
    def build_client(auth: Auth) -> tweepy.Client:
        return tweepy.Client(
            consumer_key=auth.consumer_key,
            consumer_secret=auth.consumer_secret,
            access_token=auth.token,
            access_token_secret=auth.secret,
        )

    def scrap(self, limit: Optional[int] = None) -> Iterator[Tuple[str, str]]:
        return self.scraper.scrap(limit, self.client)

    def post(self, data: str) -> str:
        return tweet(data, self.client)

    def score(self, post_id: str) -> float:
        return self.scorer.score(post_id, self.client)
