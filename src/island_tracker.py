#!/usr/bin/env python3
"""Geographical shapes"""

import os
import logging
import argparse

import tweepy

from amti import amti

def configure_logger(module_name: str) -> logging.Logger:
    """Configure the logger"""
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

LOG = configure_logger(__name__)

# pylint: disable=too-few-public-methods
class Twitter:
    """Wrapper for the Twitter API"""

    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(os.environ["API_KEY"],
                                   os.environ["API_SECRET"])
        auth.set_access_token(os.environ["ACCESS_TOKEN"],
                              os.environ["ACCESS_TOKEN_SECRET"])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    @staticmethod
    def _compose(island: amti.Island) -> dict[str, str | float]:
        """Compose a status dictionary compatible with api.status_update"""
        name_tw_en, name_tw_zh = island.names["Taiwan"].split(", ", maxsplit=1)

        if island.title == name_tw_en:
            name = island.title + ", " + name_tw_zh
        else:
            name = island.title + " / " + island.names["Taiwan"]

        text = f"{name} ({island.geo.lat:.4f}, {island.geo.long:.4f}). {island.url}"
        return {"status": text, "lat": island.geo.lat, "long": island.geo.long}

    def update(self, island: amti.Island, dry_run: bool = False) -> tweepy.models.Status:
        """Post tweet for shape"""
        composition = self._compose(island)
        LOG.info("Selecting %s", island.names["Taiwan"])

        if dry_run:
            return tweepy.models.Status

        return self.api.update_status(**composition)

def main() -> None:
    """Entry point"""
    parser = argparse.ArgumentParser(description="Tweet an island")
    parser.add_argument("-n", "--dry-run", action="store_true")
    args = parser.parse_args()

    twitter = Twitter()

    amti_instance = amti.AMTI()

    island = amti_instance.random_island()
    tweet = twitter.update(island, args.dry_run)

    try:
        LOG.info("\"%s\" at %s", tweet.text, tweet.place)
    except AttributeError:
        if not args.dry_run:
            raise

if __name__ == "__main__":
    main()
