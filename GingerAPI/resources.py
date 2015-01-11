import decimal
import endpoints
from exceptions import *


class AttrDict(dict):
    def load(self, payload):
        if not isinstance(payload, dict):
            raise GingerAPIError('Error loading attributed dict %s' % self)

        for key, value in payload.iteritems():
            setattr(self, key, value)

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        self.pop(attr, None)

    def __init__(self, result):
        self.load(result)

    def __repr__(self):
        try:
            return '<%s %s>' % (self.__class__.__name__, self.id if self.id else '')
        except KeyError as e:
            return '<%s>' % self.__class__.__name__


class Merchant(AttrDict):
    def __init__(self, gapi, result):
        # fill properties
        self.load(result)

        # define endpoint structure
        self.users = endpoints.Users(gapi, self.id)
        self.projects = endpoints.Projects(gapi, self.id)
        self.balances = endpoints.Balances(gapi, self.id)


class IdealIssuer(AttrDict):
    pass


class Order(AttrDict):
    def __init__(self, gapi, result):
        # fill properties
        result['amount'] = decimal.Decimal(float(result['amount']) / 100)
        self.load(result)

        # for consistency we remove the property as it is also an endpoint
        del self.transactions

        # define endpoint structure
        self.transactions = endpoints.Transactions(gapi, self.id)


class Partner(AttrDict):
    def __init__(self, gapi, result):
        # fill properties
        self.load(result)

        # define endpoint structure
        self.merchants = endpoints.PartnerMerchants(gapi, self.id)


class User(AttrDict):
    pass


class Project(AttrDict):
    pass


class Transaction(AttrDict):
    pass


class Refund(AttrDict):
    pass


class Balance(AttrDict):
    pass
