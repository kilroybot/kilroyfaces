from abc import ABC, abstractmethod
from typing import Iterator, Optional, Tuple

import tweepy

from kilroyfaces.twitter.utils import (
    get_current_user_id,
    get_follower_ids,
    get_user_tweets,
    map_tweet,
)


class TweetScraper(ABC):
    @abstractmethod
    def scrap(
        self, limit: Optional[int], client: tweepy.Client
    ) -> Iterator[Tuple[str, str]]:
        pass


class FollowingScraper(TweetScraper):
    def scrap(
        self, limit: Optional[int], client: tweepy.Client
    ) -> Iterator[Tuple[str, str]]:
        user_id = get_current_user_id(client)
        for follower_id in get_follower_ids(user_id, client):
            for tweet in get_user_tweets(follower_id, client):
                yield map_tweet(tweet)
