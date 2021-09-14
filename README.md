# discord-sidebar-price-bot
A trimmed down fork of [edenau/discord-sidebar-price-bot](https://github.com/edenau/discord-sidebar-price-bot), 
this script runs a Discord bot that pulls live data at intervals from the Tezos blockchain.

It currently supports:

- **QUIPUSWAP PAIRS** data from the Tezos blockchain using a node of your choice.
- **XTZ Price** in USD from the Harbinger oracle

## Dependencies
Recommended `Python 3.7`, although it should support `Python >=3.5 <=3.9`. Install all dependencies:
```
pip3 install -r requirements.txt
```

## Test & Run
### Price Bot

1. Configure [crypto_config.yaml](crypto_config.yaml) using the template provided. 
It requires a unique Discord bot key and (non-unique) Guild ID per bot. You also need a Quipuswap AMM contract and a Tezos node address.


2. Add your bot to your Discord server.


3. Run a cryptocurrency price bot:
```
python3 crypto_run.py -t XTZ
```

## Deploy
Once you are familiar with running a single sidebar bot, you can run multiple bots concurrently by calling `./bot.sh` and kill all bots by calling `./kill.sh`. You might want to modify the commands in `./bot.sh` to suit your own needs.
