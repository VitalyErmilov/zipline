
"""
Simple example taken from here:
https://github.com/quantopian/zipline/blob/master/zipline/examples/dual_ema_talib.py,
and modified to work in stand-alone mode.  (Not from command line Zipline tool)

Will be converted to use live data instead of backtest data.

Created by Peter Harrington (pbharrin) on 4/13/17.
"""

from zipline import TradingAlgorithm
from zipline.data.data_portal import DataPortal
from zipline.finance.trading import TradingEnvironment
from zipline.live import IBBrokerClient
from zipline.utils.factory import create_simulation_parameters
from zipline.utils.calendars import get_calendar
from zipline.pipeline.loaders import USEquityPricingLoader
from zipline.pipeline.data.equity_pricing import USEquityPricing
from zipline.data.bundles.core import load
from zipline.api import symbol, order  # used in handle_data
from talib import EMA


import os
import re
from time import time
import pandas as pd

CAPITAL_BASE = 1.0e6


def makeTS(date_str):
    """creates a Pandas DT object from a string"""
    return pd.Timestamp(date_str, tz='utc')


def parse_sqlite_connstr(db_URL):
    """parses out the db connection string (needed to make a TradingEnvironment"""
    _, connstr = re.split(r'sqlite:///', str(db_URL), maxsplit=1,)
    return connstr


def make_choose_loader(pl_loader):
    def cl(column):
        if column in USEquityPricing.columns:
            return pipeline_loader
        raise ValueError("No PipelineLoader registered for column %s." % column)
    return cl


if __name__ == '__main__':
    # create broker
    broker = IBBrokerClient()
    # TODO: need to pass broker into the relevant classes, and change those classes to be live versions

    # load the bundle,
    bundle_data = load('quantopian-quandl', os.environ, None)
    cal = bundle_data.equity_daily_bar_reader.trading_calendar.all_sessions
    pipeline_loader = USEquityPricingLoader(bundle_data.equity_daily_bar_reader, bundle_data.adjustment_reader)
    choose_loader = make_choose_loader(pipeline_loader)

    env = TradingEnvironment(asset_db_path=parse_sqlite_connstr(bundle_data.asset_finder.engine.url))

    data = DataPortal(
        env.asset_finder, get_calendar("NYSE"),
        first_trading_day=bundle_data.equity_minute_bar_reader.first_trading_day,
        equity_minute_reader=bundle_data.equity_minute_bar_reader,
        equity_daily_reader=bundle_data.equity_daily_bar_reader,
        adjustment_reader=bundle_data.adjustment_reader,
    )

    start = makeTS("2015-11-01"); end = makeTS("2016-11-01")  # this can go anywhere before the TradingAlgorithm


    def initialize(context):
        context.asset = symbol('AAPL')
        # To keep track of whether we invested in the stock or not
        context.invested = False


    def handle_data(context, data):
        trailing_window = data.history(context.asset, 'price', 40, '1d')  # the default bundle is daily data
        if trailing_window.isnull().values.any():
            return
        short_ema = EMA(trailing_window.values, timeperiod=20)
        long_ema = EMA(trailing_window.values, timeperiod=40)

        buy = False
        sell = False

        if (short_ema[-1] > long_ema[-1]) and not context.invested:
            order(context.asset, 100)
            context.invested = True
            buy = True
        elif (short_ema[-1] < long_ema[-1]) and context.invested:
            order(context.asset, -100)
            context.invested = False
            sell = True


    # the actual running of the backtest happens in the TradingAlgorithm object
    bt_start = time()
    perf = TradingAlgorithm(
        env=env,
        get_pipeline_loader=choose_loader,
        sim_params=create_simulation_parameters(
            start=start,
            end=end,
            capital_base=CAPITAL_BASE,
            data_frequency='daily',
        ),
        **{
            'initialize': initialize,
            'handle_data': handle_data,
            'before_trading_start': None,
            'analyze': None,
        }
    ).run(data, overwrite_sim_params=False,)
    bt_end = time()

    print(perf['portfolio_value'])
    print("The backtest took %0.2f seconds to run." % (bt_end - bt_start))
    print("all done boss")