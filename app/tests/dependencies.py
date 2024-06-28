''' Contains the dependencies for testing '''

class MockResponse:
    ''' Mock response class to mock requests.Response '''
    def __init__(self, status_code, json_data, url = None):
        self.json_data = json_data
        self.url = url
        self.status_code = status_code

    def json(self):
        ''' Mock of requests.Response.json function '''
        return self.json_data
