

class GingerAPIError(StandardError):
    """
    Default Error of the API wrapper
    """
    def __init__(self, status=None, type=None, value=None):
        self.status = status or ''
        self.type = type or ''
        self.value = value or ''

    def __repr__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__, self.status, self.type, self.value)

    def __str__(self):
        return '%s: %s %s\n%s' % (self.__class__.__name__, self.status, self.type, self.value)


class HTTPError(GingerAPIError):
    """
    Errors related to the API Call
    """
    def __init__(self, result, request):
        self.status = result['error']['status'] or ''
        self.type = result['error']['type']
        self.value = result['error']['value'] + '\n\r' + request.url
