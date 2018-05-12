# -*- coding: utf-8 -*-
from strategy import Strategy
from indicator import *
from settings import settings
import logging
import logging.config

fastlen = 19
slowlen = 27
siglen = 13

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("MACDCrossBot")

def macd_cross_strategy(ticker, ohlcv, position, balance, strategy):

    # インジケーター作成
    vmacd, vsig, vhist = macd(ohlcv.close, fastlen, slowlen, siglen, use_sma=True)

    # エントリー／イグジット
    long_entry = last(vmacd > vsig)
    short_entry = last(vmacd < vsig)
    logger.info('MACD {0:.0f} Signal {1:.0f}'.format(last(vmacd), last(vsig)))

    # ロット数計算
    qty_lot = int(balance.BTC.free * 0.01 * ticker.last)
    logger.info('LOT: ' + str(qty_lot))

    # 最大ポジション数設定
    strategy.risk.max_position_size = qty_lot

    # 注文（ポジションがある場合ドテン）
    if long_entry:
        strategy.entry('L', 'buy', qty=qty_lot, limit=ticker.bid)
    else:
        strategy.cancel('L')

    if short_entry:
        strategy.entry('S', 'sell', qty=qty_lot, limit=ticker.ask)
    else:
        strategy.cancel('S')

strategy = Strategy(macd_cross_strategy)
strategy.settings.timeframe = '1h'
strategy.settings.interval = 60
strategy.settings.apiKey = settings.apiKey
strategy.settings.secret = settings.secret
strategy.testnet.use = True
strategy.testnet.apiKey = settings.testnet_apiKey
strategy.testnet.secret = settings.testnet_secret
strategy.start()