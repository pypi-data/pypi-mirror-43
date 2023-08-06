# megaphone
[![Build Status](https://secure.travis-ci.org/theatlantic/megaphone.png?branch=master)](https://travis-ci.org/theatlantic/megaphone)

This is a Python 3 library for interacting with [the API](https://developers.megaphone.fm/) provided by [Megaphone.fm](http://megaphone.fm).

## Installation

```
pip install megaphone
```

## Usage
Basic funtionality exists to extract podcasts and episodes from "networks":

```python
from megaphone.network import NetworkClient

client = NetworkClient("secret-token", "nework id")
for podcast in client.podcasts:
    print("Podcast %s:" % podcast.title)
    for episode in podcast.episodes:
        print(episode)
```

You can also extract campaign information from "organizations":

```python
from megaphone.organization import OrganizationClient

oc = OrganizationClient("secret-token", "organization-id")
for campaign in oc.campaigns:
    print(campaign.title)
    for order in campaign.orders:
        print(order)
        for ad in order.advertisements:
            print(ad)
```


## Running Tests
To run tests:

```
pip install -r dev-requirements.txt
python -m unittest
```
