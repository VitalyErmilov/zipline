
"""
Created by Peter Harrington (pbharrin) on 4/13/17.
"""
from zipline.live.broker_client import BrokerClient


class IBBrokerClient(BrokerClient):
    """
    Broker Client for Interactive Brokers.  Requires IbPy: https://github.com/blampe/IbPy
    You can install this with `pip install IbPy2`.  For IbPy to work you will need to have a running instance of
    Trader Workstation (TWS) or IB Gateway.
    """

    def __init__(self):
        print("I have been Created, and it feels great!")