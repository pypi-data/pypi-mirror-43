# -*- coding: utf-8 -*-
"""
Created on 2017/10/3
@author: MG
"""
import logging
from datetime import datetime, timedelta
from ibats_di_trader.config import config
from ibats_common.utils.db import with_db_session
from ibats_common.backend import engines
from ibats_common.common import PositionDateType, RunMode, ExchangeName
from ibats_common.utils.mess import floor
from ibats_common.trade import TraderAgentBase, trader_agent, BacktestTraderAgentBase
from ibats_di_trader.backend import engine_md
from collections import defaultdict
from enum import Enum

logger = logging.getLogger()


class OrderType(Enum):
    """
    buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖, buy-ioc：IOC买单, sell-ioc：IOC卖单
    """
    buy_market = 'buy-market'
    sell_market = 'sell-market'
    buy_limit = 'buy-limit'
    sell_limit = 'sell-limit'
    buy_ioc = 'buy-ioc'
    sell_ioc = 'sell-ioc'


@trader_agent(RunMode.Backtest, ExchangeName.DataIntegration, is_default=False)
class BacktestTraderAgent(BacktestTraderAgentBase):
    """
    供调用模拟交易接口使用
    """

    def __init__(self, stg_run_id, **kwargs):
        super().__init__(stg_run_id, **kwargs)


if __name__ == "__main__":
    import time

    # 测试交易 下单接口及撤单接口
    # symbol, vol, price = 'ocnusdt', 1, 0.00004611  # OCN/USDT
    symbol, vol, price = 'eosusdt', 1.0251, 4.1234  # OCN/USDT

    td = BacktestTraderAgent(stg_run_id=1, run_mode_params={})
    td.open_long(symbol=symbol, price=price, vol=vol)
    order_dic_list = td.get_order(symbol=symbol)
    print('after open_long', order_dic_list)
    assert len(order_dic_list) == 1
    td.cancel_order(instrument_id=symbol)
    time.sleep(1)
    order_dic_list = td.get_order(symbol=symbol)
    print('after cancel', order_dic_list)
    assert len(order_dic_list) == 0
