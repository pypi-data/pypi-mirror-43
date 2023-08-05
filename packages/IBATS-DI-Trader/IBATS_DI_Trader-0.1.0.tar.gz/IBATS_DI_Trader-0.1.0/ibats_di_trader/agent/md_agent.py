#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/20 19:53
@File    : md_agent.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import time
from ibats_common.md import MdAgentBase, md_agent
from ibats_common.common import PeriodType, RunMode, ExchangeName
from ibats_di_trader.backend import engine_md
import pandas as pd


class MdAgentPub(MdAgentBase):

    def __init__(self, instrument_id_list, md_period: PeriodType, exchange_name, agent_name=None,
                 init_load_md_count=None, init_md_date_from=None, init_md_date_to=None, **kwargs):
        MdAgentBase.__init__(
            self, instrument_id_list, md_period, exchange_name, agent_name=agent_name,
            init_load_md_count=init_load_md_count, init_md_date_from=init_md_date_from,
            init_md_date_to=init_md_date_to, **kwargs)
        self.table_name = kwargs['table_name']
        if 'datetime_key' in kwargs:
            self.datetime_key = kwargs['datetime_key']
            self.date_key = None
            self.time_key = None
        else:
            self.datetime_key = None
            self.date_key = kwargs['date_key']
            self.time_key = kwargs['time_key']
        if 'microseconds_key' in kwargs:
            self.microseconds_key = kwargs['microseconds_key']
        else:
            self.microseconds_key = None

        self.factors = kwargs['factors'] if 'factors' in kwargs else None

    def load_history(self, date_from=None, date_to=None, load_md_count=None) -> (pd.DataFrame, dict):
        """
        从mysql中加载历史数据
        实时行情推送时进行合并后供数据分析使用
        :param date_from: None代表沿用类的 init_md_date_from 属性
        :param date_to: None代表沿用类的 init_md_date_from 属性
        :param load_md_count: 0 代表不限制，None代表沿用类的 init_load_md_count 属性，其他数字代表相应的最大加载条数
        :return: md_df 或者
         ret_data {
            'md_df': md_df, 'datetime_key': 'ts_start',
            'date_key': **, 'time_key': **, 'microseconds_key': **
            }
        """
        # 如果 init_md_date_from 以及 init_md_date_to 为空，则不加载历史数据
        if self.init_md_date_from is None and self.init_md_date_to is None:
            ret_data = {'md_df': None, 'datetime_key': self.datetime_key, 'date_key': self.date_key,
                        'time_key': self.time_key, 'microseconds_key': self.microseconds_key}
            return ret_data

        # 将sql 语句形势改成由 sqlalchemy 进行sql 拼装方式
        # sql_str = """select * from md_min_1
        #     where InstrumentID in ('j1801') and tradingday>='2017-08-14'
        #     order by ActionDay, ActionTime, ActionMillisec limit 200"""
        select_clause_str = ', '.join([f"`{item}`" for item in self.factors]) \
            if self.factors is not None and len(self.factors) > 0 else '*'
        in_clause_str = ', '.join([f"`{item}`" for item in self.instrument_id_list])
        order_desc_clause_str = (f' `{self.date_key}` DESC' if self.date_key is not None else '') + \
                                (f' `{self.datetime_key}` DESC' if self.datetime_key is not None else '') + \
                                (f' `{self.time_key}` DESC' if self.time_key is not None else '') + \
                                (f' `{self.microseconds_key}` DESC' if self.microseconds_key is not None else '')

        limit_clause_str = 'LIMIT %d' % load_md_count if self.init_load_md_count is not None else ''
        sub_sql_str = f"""SELECT {select_clause_str} FROM {self.table_name}
        WHERE {self.symbol_key} IN ({in_clause_str}) %s
        ORDER BY {order_desc_clause_str} {limit_clause_str}"""

        order_clause_str = (f' `{self.date_key}`' if self.date_key is not None else '') + \
                           (f' `{self.datetime_key}`' if self.datetime_key is not None else '') + \
                           (f' `{self.time_key}`' if self.time_key is not None else '') + \
                           (f' `{self.microseconds_key}`' if self.microseconds_key is not None else '')

        sql_str = f"""SELECT {select_clause_str} FROM (
        {sub_sql_str}
        ) t ORDER BY {order_clause_str}"""

        # 加载历史数据
        self.logger.debug("\n%s", sql_str)
        md_df = pd.read_sql(sql_str, engine_md)
        # self.md_df = md_df
        ret_data = {'md_df': md_df, 'datetime_key': self.datetime_key, 'date_key': self.date_key,
                    'time_key': self.time_key, 'microseconds_key': self.microseconds_key,
                    'symbol_key': self.symbol_key, 'close_key': 'close'}
        return ret_data


@md_agent(RunMode.Backtest, ExchangeName.DataIntegration, is_default=False)
class MdAgentBacktest(MdAgentPub):

    def __init__(self, **kwargs):
        MdAgentPub.__init__(self, **kwargs)
        self.timeout = 1

    def connect(self):
        """链接redis、初始化历史数据"""
        pass

    def release(self):
        """释放channel资源"""
        pass

    def run(self):
        """启动多线程获取MD"""
        if not self.keep_running:
            self.keep_running = True
            while self.keep_running:
                time.sleep(self.timeout)
            else:
                self.logger.info('%s job finished', self.name)
