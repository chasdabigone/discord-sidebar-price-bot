# discord-sidebar-price-bot
A trimmed down fork of [edenau/discord-sidebar-price-bot](https://github.com/edenau/discord-sidebar-price-bot), 
this script runs a Discord bot that pulls data at live intervals from the Tezos blockchain and coingecko api.

It currently supports:

- **QUIPUSWAP PAIRS** data (in USD) from the Tezos blockchain using a node of your choice.
- **XTZ Price** in USD from the coingecko API

## Dependencies
Recommended `Python 3.7`, although it should support `Python >=3.5 <=3.9`. Install all dependencies:
```
pip install -r requirements.txt
```

## Test & Run
### Price Bot
1. Cache the cryptocurrency ticker list from Coincegko by generating a *crypto_cache.json* file.
```
python crypto_cache.py -v
```

2. Configure [crypto_config.yaml](crypto_config.yaml) using the template provided. 
It requires a unique Discord bot key and (non-unique) Guild ID per bot.
1 sidebar bot per cryptocurrency (expressed by their ticker e.g. BTC, ETH, YFI). For each cryptocurrency, the price can be shown in USD, BTC, and/or ETH.

3. Sometimes multiple coins or tokens share the same ticker (e.g. UNI). In this case, modify [resolver_ambiguous_ticker()](crypto_run.py#L20) to specify the token you want.

4. Run a cryptocurrency price bot:
```
python crypto_run.py -t BTC
```
Replace the ticker `BTC` with any cryptocurrency you have configured in Step 2.

## Deploy
Once you are familiar with running a single sidebar bot, you can run multiple bots concurrently by calling `./bot.sh` and kill all bots by calling `./kill.sh`. You might want to modify the commands in `./bot.sh` to suit your own needs.
