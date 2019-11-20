# hafslund-strom-api

## About

Simple POC that gets information from the [Hafslund Strøm](https://minside.hafslundstrom.no/) API.

I don't really know how this API works/if there are any documentation available.

## Setup

```
cp config.sample.ini config.ini
vim config.ini # And modify with your details
python3 -m venv venv
. venv/bin/activate
pip install requests
```

## Example

```
import pprint

import hafslund

api = hafslund.HafslundAPI("config.ini")

pprint.pprint(api.get_facilities())
```

## Notes

### Weird consumption endpoint

If you ask for consumption data for tomorrow you obviously won't get that data. But if you keep asking for the same interval you might not get the data when available either (different date intervals will yield data). This might be due to some kind of misconfigured caching in the API?
