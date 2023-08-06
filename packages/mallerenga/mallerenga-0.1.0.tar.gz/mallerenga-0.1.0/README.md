# mallerenga

Mallerenga is a library to help managing Twitter accounts

## Installation

You can install it using `pip install` as usual:
```bash
pip install mallerenga
```

## Requirements

A Twitter account with consumer key and secret and access token and secret is required.
These credentials must be provided in the following environment variables:
- `TWITTER_CONSUMER_KEY`: Consumer key
- `TWITTER_CONSUMER_SECRET`: Consumer secret
- `TWITTER_ACCESS_TOKEN`: Access token
- `TWITTER_ACCESS_TOKEN_SECRET`: Access token secret

## Usage

### As a module

Mallerenga is intended to be user mostly as a module:
```python
from mallerenga.twitter.twitter import Twitter


twitter = Twitter()
status = twitter.tweet(msg)
print(status.link)
```

### As a command

To update the Twitter status, use the following command:
```
mallerenga New status message
```
