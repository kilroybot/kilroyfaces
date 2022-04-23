from typing import Any, Dict, List, Tuple

import tweepy


def tweet(text: str, client: tweepy.Client) -> str:
    response = client.create_tweet(text=text)
    return str(response.data["id"])


def get_current_user_id(client: tweepy.Client) -> str:
    response = client.get_me()
    return str(response.data["id"])


def get_follower_ids(user_id: str, client: tweepy.Client) -> List[str]:
    response = client.get_users_following(id=user_id, user_auth=True)
    return [str(follower["id"]) for follower in response.data or []]


def get_user_tweets(
    user_id: str, client: tweepy.Client
) -> List[Dict[str, Any]]:
    response = client.get_users_tweets(id=user_id, user_auth=True)
    return response.data or []


def map_tweet(tweet: Dict[str, Any]) -> Tuple[str, str]:
    return str(tweet["id"]), tweet["text"]
