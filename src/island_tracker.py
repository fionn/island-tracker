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
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

    @staticmethod
    def _compose(island: amti.Island) -> dict:
        """Compose a status dictionary compatible with api.status_update"""
        text = "yolo"
        return {"status": text, "lat": island.geo.lat, "long": island.geo.long}

    def update(self, island: amti.Island, dry_run: bool = False) -> tweepy.Status:
        """Post tweet for shape"""
        composition = self._compose(island)
        LOG.info("Selecting %s", island.name["Taiwan"])

        if dry_run:
            return tweepy.Status

        with island.img_file.open("rb") as img_fd:
            media = self.api.media_upload(filename=island.img_file.name,
                                          file=img_fd)

        # Not implemented yet, wait for > v3.8.0
        #self.api.create_media_metadata(media.media_id, f"{shape.caption.en}")
        return self.api.update_status(**composition, media_ids=[media.media_id])

def main() -> None:
    """Entry point"""
    parser = argparse.ArgumentParser(description="Tweet shapes")
    parser.add_argument("-n", "--dry-run", action="store_true")
    args = parser.parse_args()

    twitter = Twitter()

    amti_instance = amti.AMTI("island-tracker/china")

    island = amti_instance.random_island()
    tweet = twitter.update(island, args.dry_run)

    try:
        LOG.info("\"%s\" from %s", tweet.text, tweet.place.full_name)
    except AttributeError:
        if not args.dry_run:
            raise

if __name__ == "__main__":
    main()
