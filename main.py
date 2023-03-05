import time
import hashlib
import hmac
import base64
import ssl
import logging
import aiohttp
import asyncio
import datetime as dt
from random import choice
import aiohttp_socks
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
import kucoin_chains


logging.basicConfig(level=logging.INFO, filename='your_name.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

proxy_list = [
    # your proxies
    # for example
    'socks5://z0FU9G:LTSXrt@47.4.138.169:8000',
    'socks5://NPmnKq:tLNh4y@169.81.202.228:8000',
]

headers = {
    'user-agent': UserAgent().random
}

crypto_settings = {
    'admin':
        {
            'interval': 15,
            'percent': 0,
            'volume': 10000,
            'order': 10,
            'run': False
        }
}

async def binance():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.binance.com/api/v3/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.binance.com/api/v3/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        binance_price = dict()
        for crypto in response:
            if crypto.get('bidPrice') not in ("", None) and crypto.get('askPrice') not in ("", None):
                if float(crypto.get('bidPrice')) > 0 and float(crypto.get('askPrice')) > 0:
                    if crypto.get('symbol')[-4:] == 'USDT':
                        if float(crypto.get('quoteVolume')) > crypto_settings.get('admin')['volume']:
                            binance_price.update({crypto.get('symbol').upper():
                                                      [float(crypto.get('bidPrice')) * 0.999,
                                                       float(crypto.get('askPrice')) * 1.001]})
        return binance_price
    except (AttributeError, TypeError):
        return None

async def huobi():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.huobi.pro/market/tickers', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.huobi.pro/market/tickers', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        huobi_price = dict()
        for crypto in response['data']:
            if crypto.get('bid') not in ("", None) and crypto.get('ask') not in ("", None):
                if float(crypto.get('bid')) > 0 and float(crypto.get('ask')) > 0:
                    if crypto.get('symbol')[-4:] == 'usdt':
                        if float(crypto.get('vol')) > crypto_settings.get('admin')['volume']:
                            huobi_price.update({crypto.get('symbol').upper():
                                        [float(crypto.get('bid')) * 0.998, float(crypto.get('ask')) * 1.002]})
        return huobi_price
    except (AttributeError, TypeError):
        return None

async def bybit():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.bybit.com/spot/quote/v1/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.bybit.com/spot/quote/v1/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        bybit_price = dict()
        for crypto in response['result']:
            if crypto.get('bestBidPrice') not in ("", None) and crypto.get('bestAskPrice') not in ("", None):
                if float(crypto.get('bestBidPrice')) > 0 and float(crypto.get('bestAskPrice')) > 0:
                    if crypto.get('symbol')[-4:] == 'USDT':
                        if float(crypto.get('quoteVolume')) > crypto_settings.get('admin')['volume']:
                            bybit_price.update({crypto.get('symbol').upper():
                                [float(crypto.get('bestBidPrice')) * 0.999, float(crypto.get('bestAskPrice')) * 1.001]})
        return bybit_price
    except (AttributeError, TypeError):
        return None

async def kucoin():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.kucoin.com/api/v1/market/allTickers', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.kucoin.com/api/v1/market/allTickers', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        kucoin_price = dict()
        for crypto in response['data']['ticker']:
            if '3' not in crypto.get('symbol') and '5' not in crypto.get('symbol'):
                if crypto.get('buy') not in ("", None) and crypto.get('sell') not in ("", None):
                    if float(crypto.get('buy')) > 0 and float(crypto.get('sell')) > 0:
                        if crypto.get('symbol')[-4:] == 'USDT':
                            if float(crypto.get('volValue')) > crypto_settings.get('admin')['volume']:
                                kucoin_price.update({crypto.get('symbol').upper().replace('-', ''):
                                             [float(crypto.get('buy')) * 0.999, float(crypto.get('sell')) * 1.001]})
        return kucoin_price
    except (AttributeError, TypeError):
        return None

async def gateio():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.gateio.ws/api/v4/spot/tickers', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.gateio.ws/api/v4/spot/tickers', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        gateio_price = dict()
        for crypto in response:
            if '3' not in crypto.get('currency_pair') and '5' not in crypto.get('currency_pair'):
                if crypto.get('highest_bid') not in ("", None) and crypto.get('lowest_ask') not in ("", None):
                    if float(crypto.get('highest_bid')) > 0 and float(crypto.get('lowest_ask')) > 0:
                        if crypto.get('currency_pair')[-4:] == 'USDT':
                            if float(crypto.get('quote_volume')) > crypto_settings.get('admin')['volume']:
                                gateio_price.update({crypto.get('currency_pair').upper().replace('_', ''):
                                   [float(crypto.get('highest_bid')) * 0.998, float(crypto.get('lowest_ask')) * 1.002]})
        return gateio_price
    except (AttributeError, TypeError):
        return None

async def mexc():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.mexc.com/api/v3/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.mexc.com/api/v3/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        mexc_price = dict()
        for crypto in response:
            if '3' not in crypto.get('symbol') and '5' not in crypto.get('symbol'):
                if crypto.get('bidPrice') not in ("", None) and crypto.get('askPrice') not in ("", None):
                    if float(crypto.get('bidPrice')) > 0 and float(crypto.get('askPrice')) > 0:
                        if crypto.get('symbol')[-4:] == 'USDT':
                            if float(crypto.get('quoteVolume')) > crypto_settings.get('admin')['volume']:
                                mexc_price.update({crypto.get('symbol'):
                                        [float(crypto.get('bidPrice')) * 0.998, float(crypto.get('askPrice')) * 1.002]})
        return mexc_price
    except (AttributeError, TypeError):
        return None

async def okx():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://www.okx.com/api/v5/market/tickers?instType=SPOT', headers=headers) \
                    as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.okx.com/api/v5/market/tickers?instType=SPOT', headers=headers) \
                    as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    try:
        okx_price = dict()
        for crypto in response['data']:
            if crypto.get('bidPx') not in ("", None) and crypto.get('askPx') not in ("", None):
                if float(crypto.get('bidPx')) > 0 and float(crypto.get('askPx')) > 0:
                    if crypto.get('instId')[-4:] == 'USDT':
                        if float(crypto.get('volCcy24h')) > crypto_settings.get('admin')['volume']:
                            okx_price.update({crypto.get('instId').upper().replace('-', ''):
                                      [float(crypto.get('bidPx')) * 0.999, float(crypto.get('askPx')) * 1.001]})
        return okx_price
    except (AttributeError, TypeError):
        return None

cex_func = {
    'binance': binance,
    'huobi': huobi,
    'bybit': bybit,
    'kucoin': kucoin,
    'gateio': gateio,
    'mexc': mexc,
    'okx': okx,
    }

async def binance_chain():
    api_key = '' # your api_key
    secret_key = '' # your secret_key
    base_url = 'https://api.binance.com'

    query_string = f'timestamp={int(time.time() * 1000)}'
    url = (base_url + '/sapi/v1/capital/config/getall' + '?' + query_string + '&signature=' +
            hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest())

    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            session.headers.update({'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': api_key})
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            session.headers.update({'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': api_key})
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    chain_rename = {
        'BSC': 'BEP20',
        'BNB': 'BEP2',
        'ETH': 'ERC20',
        'TRX': 'TRC20',
        'APT': 'APTOS'
    }

    try:
        binance_status = dict()
        for value in response:
            binance_status.update({value.get('coin'): {}})
            for value_ in value.get('networkList'):
                if value_.get('network') in chain_rename:
                    chain = chain_rename[value_.get('network')]
                else:
                    chain = value_.get('network')
                binance_status[value.get('coin')].update({chain:
                         [value_.get('depositEnable'), value_.get('withdrawEnable'), float(value_.get('withdrawFee'))]})
        return binance_status
    except (AttributeError, TypeError, KeyError):
        return None

async def huobi_chain():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.huobi.pro/v2/reference/currencies', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.huobi.pro/v2/reference/currencies', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    chain_rename = {
        'AVAXCCHAIN': 'AVAXC',
        'ARBITRUMONE': 'ARBITRUM',
        'OP': 'OPTIMISM',
        'ATOM1': 'ATOM',
        'C-CHAIN': 'AVAXC',
        'CCHAIN': 'AVAXC',
        'APT': 'APTOS',
        'MOONBEAM': 'GLMR',
        'WAX1': 'WAX'
    }

    try:
        huobi_status = dict()
        for value in response['data']:
            huobi_status.update({value.get('currency').upper(): {}})
            for value_ in value.get('chains'):
                if value_.get('transactFeeWithdraw') not in ('', None):
                    if value_.get('displayName') in chain_rename:
                        chain = chain_rename[value_.get('displayName')]
                    else:
                        chain = value_.get('displayName')
                    if value_.get('depositStatus') == 'allowed':
                        deposit = True
                    else:
                        deposit = False
                    if value_.get('withdrawStatus') == 'allowed':
                        withdrawal = True
                    else:
                        withdrawal = False
                    huobi_status[value.get('currency').upper()].update({chain: [deposit, withdrawal,
                                                                            float(value_.get('transactFeeWithdraw'))]})
        return huobi_status
    except (AttributeError, TypeError, KeyError):
        return None

async def bybit_chain():
    api_key = '' # your api_key
    secret_key = '' # your secret_key

    recv_window = str(5000)
    time_stamp = str(int(time.time() * 10 ** 3))
    param_str = str(time_stamp) + api_key + recv_window
    hash = hmac.new(bytes(secret_key, 'utf-8'), param_str.encode('utf-8'), hashlib.sha256)
    signature = hash.hexdigest()
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    url = ('https://api.bybit.com' + '/asset/v3/private/coin-info/query')

    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    chain_rename = {
        'BSC (BEP20)': 'BEP20',
        'Bitcoin Cash': 'BCH',
        'Arbitrum One': 'ARBITRUM',
        'Dogecoin': 'DOGE',
        'Waves': 'WAVES',
        'Terra Classic': 'LUNC',
        'Terra': 'LUNA',
        'BNB (BEP2)': 'BEP2',
        'Caduceus': 'CMP',
        'Ethereum Classic': 'ETC',
        'Optimism': 'OPTIMISM',
        'Stellar Lumens': 'XLM',
        'Filecoin': 'FIL',
        'Klaytn': 'KLAY',
        'zkSync': 'ZKSYNC',
    }

    try:
        bybit_status = dict()
        for value in response['result']['rows']:
            bybit_status.update({value.get('name'): {}})
            for value_ in value.get('chains'):
                if value_.get('withdrawFee') not in ('', None):
                    if value_.get('chainType') in chain_rename:
                        chain = chain_rename[value_.get('chainType')]
                    else:
                        chain = value_.get('chainType')
                    if value_.get('chainDeposit') == '1':
                        deposit = True
                    else:
                        deposit = False
                    if value_.get('chainWithdraw') == '1':
                        withdrawal = True
                    else:
                        withdrawal = False
                    bybit_status[value.get('name')].update({chain: [deposit, withdrawal,
                                                                    float(value_.get('withdrawFee'))]})
        return bybit_status
    except (AttributeError, TypeError, KeyError):
        return None

async def kucoin_chain():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.kucoin.com/api/v1/currencies', headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.kucoin.com/api/v1/currencies', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    kucoin_status = kucoin_chains.chains

    try:
        for value in response['data']:
            if value.get('currency') in kucoin_status:
                key = list(kucoin_status[value.get('currency')].keys())
                kucoin_status[value.get('currency')][key[-1]] = [value.get('isDepositEnabled'),
                                                                 value.get('isWithdrawEnabled'),
                                                                 float(value.get('withdrawalMinFee'))]
        return kucoin_status
    except (AttributeError, TypeError, KeyError):
        return None

async def gateio_chain():
    api_key = '' # your api_key
    secret_key = '' # your secret_key

    t = time.time()
    m = hashlib.sha512()
    m.update(('').encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % ('GET', '/api/v4/wallet/withdraw_status', '', hashed_payload, t)
    sign = hmac.new(secret_key.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    gen_sign = {'KEY': api_key, 'Timestamp': str(t), 'SIGN': sign}
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    sign_headers = gen_sign
    headers.update(sign_headers)
    url = ('https://api.gateio.ws/api/v4/wallet/withdraw_status')

    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://api.gateio.ws/api/v4/spot/currencies') as response1:
                response1 = await response1.json()
            async with session.get(url, headers=headers) as response2:
                response2 = await response2.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.gateio.ws/api/v4/spot/currencies') as response1:
                response1 = await response1.json()
            async with session.get(url, headers=headers) as response2:
                response2 = await response2.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError,
            aiohttp.ServerConnectionError, aiohttp.ServerTimeoutError, asyncio.exceptions.TimeoutError):
        return None

    chain_rename = {
        'BSC': 'BEP20',
        'ETH': 'ERC20',
        'ARB': 'ARBITRUM',
        'AVAX_C': 'AVAXC',
        'BNB': 'BEP2',
        'TRX': 'TRC20',
        'APT': 'APTOS'
    }

    try:
        gateio_status = dict()
        for value in response1:
            if '_' in value.get('currency'):
                coin = value.get('currency').split('_')[0]
            else:
                coin = value.get('currency')
            if value.get('chain') in chain_rename:
                chain = chain_rename[value.get('chain')]
            else:
                chain = value.get('chain')
            if coin not in gateio_status:
                gateio_status.update({coin: {chain: [not value.get('deposit_disabled'),
                                                     not value.get('withdraw_disabled'), None]}})
            else:
                gateio_status[coin].update({chain: [not value.get('deposit_disabled'),
                                                    not value.get('withdraw_disabled'), None]})

        for value_ in response2:
            if value_.get('currency') in gateio_status:
                if list(value_.keys())[-1] == 'withdraw_fix_on_chains':
                    for chain in value_.get('withdraw_fix_on_chains'):
                        if chain in chain_rename:
                            chain_ = chain_rename.get(chain)
                        else:
                            chain_ = chain
                        if chain_ in gateio_status[value_.get('currency')]:
                            gateio_status[value_.get('currency')][chain_][2] = float(
                                value_.get('withdraw_fix_on_chains')[chain])
        return gateio_status
    except (AttributeError, TypeError, KeyError):
        return None

async def mexc_chain():
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://www.mexc.com/open/api/v2/market/coin/list', headers=headers) as response:
                response = await response.json()
    except (ssl.SSLError, ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.mexc.com/open/api/v2/market/coin/list', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    chain_rename = {
        'BEP20(BSC)': 'BEP20',
        'Chiliz Chain(CHZ)': 'CHZ',
        'AVAX_CCHAIN': 'AVAXC',
        'Arbitrum One': 'ARBITRUM',
        'OP': 'OPTIMISM',
        'AVAX_XCHAIN': 'AVAXX',
        'Khala': 'KHALA',
        'LUNA2': 'LUNA',
        'UGAS(Ultrain)': 'UGAS',
        'MEVerse': 'MEVERSE',
        'RONIN': 'RON',
        'FLARE': 'FLR'
    }

    try:
        mexc_status = dict()
        for value in response['data']:
            mexc_status.update({value.get('currency'): {}})
            for value_ in value.get('coins'):
                if value_.get('chain') in chain_rename:
                    chain = chain_rename[value_.get('chain')]
                else:
                    chain = value_.get('chain')
                mexc_status[value.get('currency')].update({chain: [value_.get('is_deposit_enabled'),
                                                        value_.get('is_withdraw_enabled'), float(value_.get('fee'))]})
        return mexc_status
    except (AttributeError, TypeError, KeyError):
        return None

async def okx_chain():
    api_key = '' # your api_key
    secret_key = '' # your secret_key
    password = '' # your password
    url = 'https://aws.okex.com/api/v5/asset/currencies'

    cur_time = (dt.datetime.utcnow().isoformat()[:-3] + 'Z')
    message = (str(cur_time) + 'GET' + '/api/v5/asset/currencies' + '')
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    signature = base64.b64encode(d).decode('utf8')
    headers = {
        'CONTENT-TYPE': 'application/json',
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': str(cur_time),
        'OK-ACCESS-PASSPHRASE': password
    }

    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (ConnectionResetError, ConnectionRefusedError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

    chain_rename = {
        'Polygon': 'MATIC',
        'Avalanche C-Chain': 'AVAXC',
        'Bitcoin': 'BTC',
        'Arbitrum one': 'ARBITRUM',
        'Optimism': 'OPTIMISM',
        'EthereumPoW': 'ETHW',
        'Litecoin': 'LTC',
        'BitcoinCash': 'BCH',
        'Ethereum Classic': 'ETC',
        'Acala': 'ACALA',
        'Cardano': 'ADA',
        'Algorand': 'ALGO',
        'Terra Classic': 'LUNC',
        'Aptos': 'APTOS',
        'Arweave': 'AR',
        'Chiliz': 'CHZ',
        'Astar': 'ASTAR',
        'Cosmos': 'ATOM',
        'Avalanche X-Chain': 'AVAXX',
        'BSC': 'BEP20',
        'Bitcoin Diamond': 'BCD',
        'Klaytn': 'KLAY',
        'BitcoinGold': 'BTG',
        'Bytom': 'BTM',
        'Conflux': 'CFX',
        'CyberMiles': 'CMT',
        'Casper': 'CSPR',
        'Cortex': 'CTXC',
        'Decred': 'DCR',
        'Digibyte': 'DGB',
        'Dogecoin': 'DOGE',
        'Polkadot': 'DOT',
        'Elrond': 'EGLD',
        'Eminer': 'EM',
        'Filecoin': 'FIL',
        'Flare': 'FLR',
        'Fusion': 'FSN',
        'Fantom': 'FTM',
        'Solana': 'SOL',
        'Moonbeam': 'GLMR',
        'Hedera': 'HBAR',
        'HyperCash': 'HC',
        'Helium': 'HNT',
        'Kadena': 'KDA',
        'Kusama': 'KSM',
        'PlatON': 'LAT',
        'Lisk': 'LSK',
        'Terra': 'LUNA',
        'Metis': 'METIS',
        'Mina': 'MINA',
        'Moonriver': 'MOVR',
        'Nebulas': 'NAS',
        'Harmony': 'ONE',
        'Ontology': 'ONT',
        'Khala': 'KHALA',
        'Quantum': 'QAU',
        'Stellar Lumens': 'XLM',
        'Ronin': 'RON',
        'Ravencoin': 'RVM',
        'Siacoin': 'SC',
        'Ripple': 'XRP',
        'l-Stacks': 'STX',
        'Theta': 'THETA',
        'TrueChain': 'TRUE',
        'Wax': 'WAXP',
        'Chia': 'XCH',
        'New Economy Movement': 'NEM',
        'Monero': 'XMR',
        'Nano': 'XNO',
        'Tezos': 'XTZ',
        'Zcash': 'ZEC',
        'Horizen': 'ZEN',
        'Zilliqa': 'ZIL',
        'Step Network': 'STEP',
        'WAXP': 'WAX',
        'ICON': 'ICX'
    }

    try:
        okx_status = dict()
        for value in response['data']:
            if value.get('chain').replace(f'{value.get("ccy")}-', '') in chain_rename:
                chain = chain_rename[value.get('chain').replace(f'{value.get("ccy")}-', '')]
            else:
                chain = value.get('chain').replace(f'{value.get("ccy")}-', '')
            if value.get('ccy') not in okx_status:
                okx_status.update({value.get('ccy'): {chain: [value.get('canDep'), value.get('canWd'),
                                                                float(value.get('maxFee'))]}})
            else:
                okx_status[value.get('ccy')].update({chain: [value.get('canDep'), value.get('canWd'),
                                                                float(value.get('maxFee'))]})
        return okx_status
    except (AttributeError, TypeError, KeyError):
        return None

chain_status = {
    'binance': binance_chain,
    'huobi': huobi_chain,
    'bybit': bybit_chain,
    'kucoin': kucoin_chain,
    'gateio': gateio_chain,
    'mexc': mexc_chain,
    'okx': okx_chain,
}

async def binance_qty(traiding_pair):
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.binance.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
                    as response:
                response = await response.json()
                return response
    except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.binance.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
                    as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

async def huobi_qty(traiding_pair):
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.huobi.pro/market/depth?symbol='
                                   f'{traiding_pair.lower()}&type=step0', headers=headers) as response:
                response = await response.json()
                response = response.get('tick')
                return response
    except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.huobi.pro/market/depth?symbol='
                                   f'{traiding_pair.lower()}&type=step0', headers=headers) as response:
                response = await response.json()
                response = response.get('tick')
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

async def bybit_qty(traiding_pair):
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.bybit.com/spot/v3/public/quote/depth?symbol='
                                   f'{traiding_pair}&limit=5', headers=headers) as response:
                response = await response.json()
                response = response.get('result')
                return response
    except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.bybit.com/spot/v3/public/quote/depth?symbol='
                                   f'{traiding_pair}&limit=5', headers=headers) as response:
                response = await response.json()
                response = response.get('result')
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

async def kucoin_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol='
                                   f'{traiding_pair}-USDT', headers=headers) as response:
                response = await response.json()
                response = response.get('data')
                return response
    except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol='
                                   f'{traiding_pair}-USDT', headers=headers) as response:
                response = await response.json()
                response = response.get('data')
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

async def gateio_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.gateio.ws/api/v4/spot/order_book?currency_pair='
                                   f'{traiding_pair}_USDT', headers=headers) as response:
                response = await response.json()
                return response
    except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.gateio.ws/api/v4/spot/order_book?currency_pair='
                                   f'{traiding_pair}_USDT', headers=headers) as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

async def mexc_qty(traiding_pair):
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://api.mexc.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
                    as response:
                response = await response.json()
                return response
    except (ssl.SSLError, ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.mexc.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
                    as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

async def okx_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
        connector = ProxyConnector.from_url(choice(proxy_list))
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://www.okx.com/api/v5/market/books-lite?instId='
                                   f'{traiding_pair}-USDT', headers=headers) as response:
                response = await response.json(encoding='utf-8', content_type='text/plain')
                response = response.get('data')[0]
                return response
    except (TypeError, ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
            aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.okx.com/api/v5/market/books-lite?instId='
                                   f'{traiding_pair}-USDT', headers=headers) as response:
                response = await response.json(encoding='utf-8', content_type='text/plain')
                response = response.get('data')[0]
                return response
    except (TypeError, aiohttp.ClientError, aiohttp.ClientConnectionError, asyncio.exceptions.TimeoutError):
        return None

quantity = {
    'binance': binance_qty,
    'huobi': huobi_qty,
    'bybit': bybit_qty,
    'kucoin': kucoin_qty,
    'gateio': gateio_qty,
    'mexc': mexc_qty,
    'okx': okx_qty,
}

async def url(cex_name, traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    link = {
        'binance': f'https://www.binance.com/ru-UA/trade/{traiding_pair}_USDT?theme=dark&type=spot',
        'huobi': f'https://www.huobi.com/ru-ru/exchange/{traiding_pair.lower()}_usdt',
        'bybit': f'https://www.bybit.com/uk-UA/trade/spot/{traiding_pair}/USDT',
        'kucoin': f'https://www.kucoin.com/ru/trade/{traiding_pair}-USDT?spm=kcWeb.B1homepage.Header4.1',
        'gateio': f'https://www.gate.io/trade/{traiding_pair}_USDT',
        'mexc': f'https://www.mexc.com/ru-RU/exchange/{traiding_pair}_USDT?_from=header',
        'okx': f'https://www.okx.com/ru/trade-spot/{traiding_pair.lower()}-usdt',
    }
    result = link.get(cex_name)
    return result

fees = {
    'binance': 0.999,
    'huobi': 0.998,
    'bybit': 0.999,
    'kucoin': 0.999,
    'gateio': 0.998,
    'mexc': 0.998,
    'okx': 0.999,
}

async def comparison_all():
    cex_name = ['binance', 'huobi', 'huobi', 'kucoin', 'gateio', 'mexc', 'okx']
    cex_list = list()
    cex_chain = list()

    for func in cex_name:
        cex_list_result = await cex_func.get(func)()
        cex_chain_result = await chain_status.get(func)()
        if isinstance(cex_list_result and cex_chain_result, dict):
            cex_list.append(cex_list_result)
            cex_chain.append(cex_chain_result)
        else:
            cex_name.remove(func)

    price_filter = dict()

    for i in range(len(cex_list)):
        for i_ in range(i + 1, len(cex_list)):
            price1 = cex_list[i]
            price2 = cex_list[i_]
            for crypto1 in price1:
                for crypto2 in price2:
                    if crypto1 == crypto2:
                        if price1.get(crypto2)[1] < price2.get(crypto2)[0]:
                            price_high = price2.get(crypto2)[0]
                            price_low = price1.get(crypto2)[1]
                            if crypto_settings.get('admin')['percent'] < (
                                    (price_high - price_low) / price_low) * 100 <= 50:
                                price_filter.update({crypto1: [cex_name[i], cex_name[i_]]})
                        elif price1.get(crypto2)[0] > price2.get(crypto2)[1]:
                            price_high = price1.get(crypto2)[0]
                            price_low = price2.get(crypto2)[1]
                            if crypto_settings.get('admin')['percent'] < (
                                    (price_high - price_low) / price_low) * 100 <= 50:
                                price_filter.update({crypto1: [cex_name[i_], cex_name[i]]})

    chain_filter = list()

    for traiding_pair in price_filter:
        values_list = price_filter.get(traiding_pair)
        crypto = traiding_pair.replace('USDT', '')
        chain = cex_chain[cex_name.index(values_list[0])]
        chain_ = cex_chain[cex_name.index(values_list[1])]
        if crypto in chain and crypto in chain_:
            keys = list(chain.get(crypto).keys())
            keys_ = list(chain_.get(crypto).keys())
            for key in keys:
                if isinstance(chain.get(crypto)[key][2], float) and chain.get(crypto)[key][1]:
                    if key in keys_:
                        if chain_.get(crypto)[key][0]:
                            chain_filter.append([traiding_pair, values_list[0], values_list[1], key,
                                                 chain.get(crypto)[key][2]])

    for value in chain_filter:
        amount = await quantity.get(value[1])(value[0])
        amount_ = await quantity.get(value[2])(value[0])
        if amount is not None and amount_ is not None:
            if 'asks' in amount and 'bids' in amount_:
                amount = amount['asks']
                amount_ = amount_['bids']
                if amount is not None and amount_ is not None:
                    l = min(len(amount), len(amount_))
                    qty, qty_ = list(), list()
                    price, price_ = list(), list()
                    for i in range(l):
                        if float(amount[i][0]) < float(amount_[i][0]):
                            qty.append(float(amount[i][1]))
                            qty_.append(float(amount_[i][1]))
                            price.append(float(amount[i][0]))
                            price_.append(float(amount_[i][0]))
                    if len(qty) > 0 and len(qty_) > 0:
                        min_qty = min(sum(qty), sum(qty_))
                        min_price = min(price)
                        max_price = max(price)
                        avg_price = (min_price + max_price) / 2
                        min_price_ = min(price_)
                        max_price_ = max(price_)
                        avg_price_ = (min_price_ + max_price_) / 2
                        fee = value[4]
                        profit = min_qty * fees.get(value[1])
                        profit_usd = min_qty * avg_price
                        profit_ = (profit - fee) * fees.get(value[2])
                        profit_usd_ = profit_ * avg_price_
                        if profit_usd_ > profit_usd:
                            total_profit = ((profit_usd_ - profit_usd) / profit_usd) * 100
                            total_profit = round(total_profit, 2)
                            if total_profit > crypto_settings.get('admin')['percent']:
                                text = (f'📢 {value[0]}\n'
                                            f'🔹 {value[1].capitalize()} average buying price:\n'
                                            f'🔹 {str(format(avg_price, ".12f").rstrip("0"))} 💰\n'
                                            f'🔹 ({str(format(min_price, ".12f").rstrip("0"))} -'
                                            f' {str(format(max_price, ".12f").rstrip("0"))})\n'
                                            f'🔹 Buy amount:\n'
                                            f'🔹 {round(profit, 2)} {value[0].replace("USDT", "")} -'
                                            f' {round(profit_usd, 2)} 💵\n'
                                            f'🔹 {value[2].capitalize()} average selling price:\n'
                                            f'🔹 {str(format(avg_price_, ".12f").rstrip("0"))} 💰\n'
                                            f'🔹 ({str(format(max_price_, ".12f").rstrip("0"))} -'
                                            f' {str(format(min_price_, ".12f").rstrip("0"))})\n'
                                            f'🔹 Sell amount:\n'
                                            f'🔹 {round(profit_, 2)} {value[0].replace("USDT", "")} -'
                                            f' {round(profit_usd_, 2)} 💵\n'
                                            f'🔹 Chain - {value[3]} ⚠️\n'
                                            f'🔹 Chain fee - {value[4]} {value[0].replace("USDT", "")}\n'
                                            f'🔹 Profit - {total_profit} % - {round(profit_usd_ - profit_usd, 2)} 💵')
                                print(text)

async def run_crypto():
    while crypto_settings.get('admin')['run']:
        await comparison_all()
        await asyncio.sleep(crypto_settings.get('admin')['interval'] * 60)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_crypto())
