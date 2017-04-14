
"""
Basic file to make sure you can properly connect to IB, make sure you can run this
before you try to run other code that talks to IB.

This test does not place orders, so it SHOULD NOT change your account balance.

Created by Peter Harrington (pbharrin) on 4/14/17.
"""

from ib.opt import ibConnection, message
from time import sleep


class IBConnectionTester:
    def __init__(self):
        self.found_account_value = False
        print("testing IB connection")
        self.con = ibConnection()
        self.con.register(self.my_account_handler, 'UpdateAccountValue')

        if not self.con.connect(): # start the connection
            raise Exception("cannot connect check that you are using port 7496")

    def my_account_handler(self, msg):
        #print(msg)
        if msg.key == "FundValue":
            self.found_account_value = True

    def start(self):
        self.con.reqAccountUpdates(1, '')



if __name__ == '__main__':


    testerob = IBConnectionTester()

    # register a handler for specific message types
    testerob.start()
    sleep(3)

    testerob.con.disconnect()

    if testerob.found_account_value:
        print("looks like you could connect and get the account value")
