import json
from resources import *
from exceptions import *


class Base(object):

    def __init__(self, gapi):
        self.gapi = gapi

    def __repr__(self):
        return '<%s: I\'m a red-headed endpoint, please use one of my functions >' % self.__class__.__name__

    """
    HTTP functions
    """

    def get(self, endpoint_id=None):
        if endpoint_id:
            # get single resource
            result = self.gapi.call_api('GET', self.path + '/' + endpoint_id, None, None)
            return self.resource(result)

        else:
            # get all resources
            result = self.gapi.call_api('GET', self.path, None, None)
            for i, r in enumerate(result):
                result[i] = self.resource(r)
            return result

    def post(self, data):
        try:
            data = json.dumps(data)
        except Exception as e:
            raise GingerAPIError('Error encoding parameters into JSON: "%s"' % e.message)
        result = self.gapi.call_api('POST', self.path, data, None)

        return self.resource(result)

    def put(self, endpoint_id, resource):
        # strip endpoints on resource
        attr_to_delete = list()
        for key, value in resource.iteritems():
            if isinstance(value, Base):
                attr_to_delete.append(key)
        for key in attr_to_delete:
            delattr(resource, key)

        # perform request
        try:
            data = json.dumps(resource)
        except Exception as e:
            raise GingerAPIError('Error encoding parameters into JSON: "%s"' % e.message)
        result = self.gapi.call_api('PUT', self.path + '/' + endpoint_id, data, None)

        return self.resource(result)

    def delete(self, endpoint_id):
        result = self.gapi.call_api('DELETE', self.path + '/' + endpoint_id, None, None)

        return self.resource(result)

    def options(self):
        pass

    """
    Endpoint functions
    """

    def resource(self, result=None):
        raise NotImplementedError()

    def create(self, data):
        return self.post(data)

    def all(self):
        return self.get(None)


class Merchants(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'merchants'

    def resource(self, result):
        return Merchant(self.gapi, result)


class Orders(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'orders'

    def create(self, data):
        # filter amount
        if isinstance(data['amount'], decimal.Decimal):
            data['amount'] = int(round(data['amount'] * 100))

        return self.post(data)

    def resource(self, result):
        return Order(self.gapi, result)


class IdealIssuers(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'ideal/issuers'

    def resource(self, result):
        return IdealIssuer(result)


class Partners(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'partners'

    def resource(self, result):
        return Partner(self.gapi, result)


class PartnerMerchants(Base):
    def __init__(self, gapi, partner_id):
        self.gapi = gapi
        self.path = 'partners/%s/merchants' % partner_id

    def resource(self, result):
        return Merchant(self.gapi, result)


class Users(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'merchants/%s/users' % merchant_id

    def resource(self, result):
        return User(result)


class Projects(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'merchants/%s/projects' % merchant_id

    def resource(self, result):
        return Project(result)


class Transactions(Base):
    def __init__(self, gapi, order_id):
        self.gapi = gapi
        self.path = 'orders/%s/transactions' % order_id

    def resource(self, result):
        return Transaction(result)


class Refunds(Base):
    pass


class Balances(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'reports/balance/merchants/%s' % merchant_id

    def get(self, endpoint_id=None):
        # response is not a list, but a dict in a dict. Lets transform
        result = self.gapi.call_api('GET', self.path, None, None)
        result_new = dict()
        for i, r in enumerate(result):
            if 'EUR' in result[r]:
                result_new[r] = float(result[r]['EUR']) / 100
            else:
                result_new[r] = 0
        return self.resource(result_new)

    def resource(self, result):
        return Balance(result)
