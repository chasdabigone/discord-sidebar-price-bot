"""
Run a Discord sidebar bot that shows price of a cryptocurrency
"""
# Example:
# python3 crypto_run.py -t BTC &


updateCounter = 0 #so get_blockchain() will have variable set

from typing import List

def get_blockchain():
    
    import math
    from pytezos import pytezos
    global decimals
    global quipu
    global updateCounter
    global pairPeg
    global pairPrice
    global harbingerPrice
    global config

    
    #fetch harbinger oracle price
    harbinger = pytezos.using(config['tezosNode'])
    harbinger = harbinger.contract('KT1Jr5t9UvGiqkvvsuUbPJHaYx24NzdUwNW9')
    harbingerPrice = harbinger.storage['oracleData']['XTZ-USD']()[5]
    harbingerPrice = (harbingerPrice / math.pow(10, 6))


    #for cycling between showing XTZ/pair price in peg mode
    if updateCounter == 0: 
        updateCounter = 1
    else:
        updateCounter = 0


    #get xtz and pair amounts
    pairAmt = quipu.storage['storage']['token_pool']()
    XTZamt = quipu.storage['storage']['tez_pool']()


    #calculate price and peg
    pairRatio = (XTZamt / math.pow(10, 6)) / (pairAmt / math.pow(10, decimals))
    pairPrice = harbingerPrice * pairRatio
    pairPeg = (pairPrice - 1) * 100
     
    

def main(ticker: str,
         verbose: bool = False) -> None:
    import argparse
    import math
    import json, yaml
    import discord
    import asyncio
    from pytezos import pytezos
    global pairSymbol
    global pairPeg
    global quipu
    global decimals
    global harbingerPrice
    global config

    # 1. Load config
    filename = 'crypto_config.yaml'
    with open(filename) as f:
        
        config = yaml.load(f, Loader=yaml.Loader)[ticker.upper()] # Assume tickers in yaml file are in uppercase
        if verbose:
            print(f'{ticker} data loaded from {filename}')
            



    # 2. Get Initial Blockchain Data


    try:
        #fetch quipuswap contract data
        quipu = pytezos.using(config['tezosNode'])
        quipu = quipu.contract(config['contractAddress'])

        #fetch pair data
        pairAddress = quipu.storage['storage']['token_address']()
        pairContract = pytezos.using(config['tezosNode'])
        pairContract = pairContract.contract(pairAddress)

        #find symbol of pair
        pairSymbol = pairContract.storage['token_metadata'][0]()[1]['symbol'].decode()

        #find mantissa of pair
        decimals_str = pairContract.storage['token_metadata'][0]()[1]['decimals']
        #set mantissa variable
        decimals = int(decimals_str)
    except:
        print ("error initializing contract data, retrying")
        pass
        main(ticker=args.ticker,
         verbose=args.verbose)

    # 3. Connect w the bot
    try:
        client = discord.Client()
        numUnit = len(config['priceUnit'])#this isn't implemented right now

        async def send_update(priceList, unit, numDecimalPlace=None):
            if numDecimalPlace == 0:
                numDecimalPlace = None # round(2.3, 0) -> 2.0 but we don't want ".0"


            #set name and status
            if config['stablecoinPeg'] == True:
            
                nickname = pairSymbol + ' Peg' + ' ' + str(round(pairPeg, 2)) + '%'

                if updateCounter == 1: #cycling between showing pair/XTZ
                    status = pairSymbol + ' Price' + ' ' + '$' + str(round(pairPrice, numDecimalPlace))
                else:
                    status = 'XTZ Price' + ' ' + '$' + str(round(harbingerPrice, 2))
            else:
                nickname = pairSymbol + ' ' + '$' + str(round(pairPrice, numDecimalPlace))
                status = 'XTZ ' + '$' + str(round(harbingerPrice, 2))


            await client.wait_until_ready()
            await client.get_guild(config['guildId']).me.edit(nick=nickname)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=status))
            await asyncio.sleep(config['updateFreq'] / numUnit) # in seconds
    except:
        print ("error connecting to bot, retrying")
        pass
        main(ticker=args.ticker,
         verbose=args.verbose)

    @client.event
    async def on_ready():
        """
        When discord client is ready
        """
        while True:
            try:
                # 4. Fetch contract prices
        
                priceList = get_blockchain()
            
            
            
        
                # 5. Feed it to the bot
                # max. 3 priceUnit (tried to avoid using for loop)
                await send_update(priceList, config['priceUnit'][0].lower(), config['decimalPlace'][0])
                if len(config['priceUnit']) >= 2:
                    await send_update(priceList, config['priceUnit'][1].lower(), config['decimalPlace'][1])
                if len(config['priceUnit']) >= 3:
                    await send_update(priceList, config['priceUnit'][2].lower(), config['decimalPlace'][2])
            except:
                print ("error feeding data to discord, retrying")
                pass
    try:
        client.run(config['discordBotKey'])
    except:
        pass

if __name__ == '__main__':
    import argparse
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--ticker',
                        action='store')
    parser.add_argument('-v', '--verbose',
                        action='store_true', # default is False
                        help='toggle verbose')
    args = parser.parse_args()
    main(ticker=args.ticker,
         verbose=args.verbose)
