
"""

Created by Peter Harrington (pbharrin) on 4/13/17.
"""


class BrokerClient:
    """Abstract class for defining an interface that all BrokerClients should implement.
    Example actions are: place orders, get historical data, get live bars, get tick data.
    """

    def register_universe_from_file(self, file_name):
        """loads a text file with securities listed.
        Registers for updates for each security.  """
        raise Exception("register_universe_from_file cannot be used until it has not be implemented")

    def register_security(self, security):
        """Registers with the broker that we want to receive updates for the given security.  """
        raise Exception("register_security cannot be used until it has not be implemented")