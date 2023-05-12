from idoit_api_client import API, Constants, Request


class TestClassIdoitApiClientRequest:
    """Test class idoit_api_client.Request"""

    config = {
        Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
        Constants.KEY: "c1ia5q",
        Constants.USERNAME: "admin",
        Constants.PASSWORD: "admin",
    }

    def test_constructor(self):
        api = API(self.config)
        request = Request(api)
        assert isinstance(request, Request)
