#!/usr/bin/env bash

# get from https://apps.twitter.com/
export TWITTER_CONSUMER_KEY='consumer_key'
export TWITTER_CONSUMER_SECRET='consumer_secret'
export TWITTER_ACCESS_KEY='access_key'
export TWITTER_ACCESS_TOKEN_SECRET='access_token_secret'

docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/logs:/logs neo4j:3.0 &
pip install -r requirements.txt
python main.py
