from abc import ABC, abstractmethod
from typing import Any, Dict

import tweepy


class TweetScorer(ABC):
    @abstractmethod
    def score(self, tweet_id: str, client: tweepy.Client) -> float:
        pass


class MetricsScorer(TweetScorer, ABC):
    def score(self, tweet_id: str, client: tweepy.Client) -> float:
        metric_field = self.metric_field()
        response = client.get_tweet(
            id=tweet_id, tweet_fields=metric_field, user_auth=True
        )
        return self.retrieve_score(response.data[metric_field])

    @abstractmethod
    def metric_field(self) -> str:
        pass

    @abstractmethod
    def retrieve_score(self, metrics: Dict[str, Any]) -> float:
        pass


class PublicMetricsScorer(MetricsScorer, ABC):
    def metric_field(self) -> str:
        return "public_metrics"


class NonpublicMetricsScorer(MetricsScorer, ABC):
    def metric_field(self) -> str:
        return "non_public_metrics"


class LikeScorer(PublicMetricsScorer):
    def retrieve_score(self, metrics: Dict[str, Any]) -> float:
        return metrics["like_count"]


class RetweetScorer(PublicMetricsScorer):
    def retrieve_score(self, metrics: Dict[str, Any]) -> float:
        return metrics["retweet_count"]


class ImpressionsScorer(NonpublicMetricsScorer):
    def retrieve_score(self, metrics: Dict[str, Any]) -> float:
        return metrics["impression_count"]
