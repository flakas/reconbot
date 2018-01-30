Reconbot for Eve Online [![CircleCI](https://circleci.com/gh/flakas/reconbot.svg?style=svg)](https://circleci.com/gh/flakas/reconbot)
=======================

Reconbot is a notification bot for Eve Online.
It fetches character notifications from the EVE API, filters irrelevant ones out and sends relevant ones to set Slack or Discord channels.
Notifications like SOV changes, SOV/POS/POCO/Citadel attacks.

# Setup

Reconbot was intended to be used as a base for further customizations, or integration with other systems, but it can be run via `run.py` as well.

1. Clone the repository
2. Execute `download_dump.sh`, which will download the latest Static Data Export from [Fuzzwork Enterprises](https://www.fuzzwork.co.uk/) and will store it in the current directory
3. Modify `run.py` with your EVE API keys, key groups and Slack accounts/channels.
`whitelist` will contain notification types you're interested in, and `characters` should contain entries for API keys of individual characters. For reconbot to work, `Notifications` and `NotificationTexts` XML API permissions are required.
4. Install Python dependencies with `pip install -r requirements.txt`
5. Execute `python run.py` and wait for notifications to arrive!

# Other notes

Reconbot will try to evenly spread out checking API keys over the cache expiry window (which is 30 minutes), meaning that with 2 API keys in rotation an API key will be checked every ~15 minutes, which can be useful to detect alliance or corporation-wide notifications a bit more quickly than every 30 minutes.
