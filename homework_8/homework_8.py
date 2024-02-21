from typing import List
from time import time
from dataclasses import dataclass


@dataclass
class SocialChannel:
    channel_type: str
    followers: int


@dataclass
class Post:
    message: str
    timestamp: int


class SocialNetwork:
    def post(self, channel: SocialChannel, message: str) -> None:
        pass


class Youtube(SocialNetwork):
    def post(self, channel: SocialChannel, message: str) -> None:
        pass


class Facebook(SocialNetwork):
    def post(self, channel: SocialChannel, message: str) -> None:
        pass


class Twitter(SocialNetwork):
    def post(self, channel: SocialChannel, message: str) -> None:
        pass


def post_a_message(
    channel: SocialChannel, message: str, social_network: SocialNetwork
) -> None:
    social_network.post(channel, message)


def process_schedule(
    posts: List[Post],
    channels: List[SocialChannel],
    social_network: SocialNetwork,
) -> None:
    current_time = time()
    for post in posts:
        if post.timestamp <= current_time:
            for channel in channels:
                post_a_message(channel, post.message, social_network)
