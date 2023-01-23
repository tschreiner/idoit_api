"""Top-level package for i-doit API Client for Python."""

__author__ = """Tedd Schreiner"""
__email__ = 'info@teddschreiner.de'
__version__ = '0.0.5'


from enum import Enum
from multiprocessing.sharedctypes import Value
import requests
from requests import Request as ReqRequest, Session
import json

"""Constants"""
class Constants:
    """
    Configuration: URL
    """
    URL = 'url'
    """
    Configuration: Port
    """
    PORT = 'port'
    """
    Lowest allowed port number:
    """
    PORT_MIN = 1
    """
    Highest allowed port number
    """
    PORT_MAX = 65535
    """
    Configuration: API key
    """
    KEY = 'key'
    """
    Configuration: Username
    """
    USERNAME = 'username'
    """
    Configuration: Password
    """
    PASSWORD = 'password'
    """
    Configuration: Language
    """
    LANGUAGE = 'language'
    """
    Configuration: Proxy settings
    """
    PROXY = 'proxy'
    """
    Configuration: Activate proxy settings?
    """
    PROXY_ACTIVE = 'active'
    """
    Configuration: Proxy type
    """
    PROXY_TYPE = 'type'
    """
    HTTP proxy
    """
    PROXY_TYPE_HTTP = 'HTTP'
    """
    SOCKS5 proxy
    """
    PROXY_TYPE_SOCKS5 = 'SOCKS5'
    """
    Configuration: Proxy host
    """
    PROXY_HOST = 'host'
    """
    Configuration: Proxy port
    """
    PROXY_PORT = 'port'
    """
    Configuration: Proxy username
    """
    PROXY_USERNAME = 'username'
    """
    Configuration: Proxy password
    """
    PROXY_PASSWORD = 'password'
    """
    Configuration: Disable security-related cURL options
    """
    BYPASS_SECURE_CONNECTION = 'bypassSecureConnection'

    CURLPROTO_HTTP = 1
    CURLPROTO_HTTPS = 2

"""Request"""
class API:
    """API client"""

    """Configuration"""
    _config = {}

    """cURL resource"""
    _curl = None

    """requests Session"""
    _resource = None

    """Information about last client request"""
    _last_info = {}

    """HTTP headers of last request"""
    _last_request_headers = None

    """HTTP headers of last server response"""
    _last_response_headers = None

    """Response for last request"""
    _last_response = None

    """Last request content"""
    _last_request_content = None

    """Current session identifier"""
    _session = None

    """cURL options"""
    _options = {}

    """Counter for JSON-RPC request identifiers"""
    _id = 0

    """Composer Information about this project"""
    _composer = {}


    def __init__(self, config):
        """Constructor"""
        self._config = config
        self._test_config()
        self._set_composer_options()
        self._set_curl_options()

    def _set_curl_options(self):
        """Sets cURL options"""
        self._options = {
            "CURLOPT_FAILONERROR": True,
            # Follow (only) 301s and 302s:
            "CURLOPT_FOLLOWLOCATION": True,
            "CURLOPT_POSTREDIR": (1 | 2),
            "CURLOPT_FRESH_CONNECT": True,
            "CURLOPT_HEADER": True,
            "CURLINFO_HEADER_OUT": True,
            "CURLOPT_CUSTOMREQUEST": 'POST',
            "CURLOPT_RETURNTRANSFER": True,
            "CURLOPT_PORT": self._config[Constants.PORT],
            "CURLOPT_REDIR_PROTOCOLS": Constants.CURLPROTO_HTTP or Constants.CURLPROTO_HTTPS,
            "CURLOPT_ENCODING": 'application/json',
            "CURLOPT_URL": self._config[Constants.URL],
            # In seconds:
            "CURLOPT_CONNECTTIMEOUT": 10,
            "CURLOPT_HTTPHEADER": {
                "Content-Type": "application/json",
                #"Expect": "application/json"
            }
        }

        if self._config.get(Constants.PROXY) is not None:
            if self._config[Constants.PROXY] is not None and self._config[Constants.PROXY][Constants.PROXY_ACTIVE]:
                self._config['CURLOPT_PROXY'] = self._config[Constants.PROXY][Constants.PROXY_HOST]
                self._options['CURLOPT_PROXYPORT'] = self._config[Constants.PROXY][Constants.PROXY_PORT]

                if self._config[Constants.PROXY][Constants.PROXY_USERNAME] is not None and isinstance(self._config[Constants.PROXY][Constants.PROXY_USERNAME], str) and self._config[Constants.PROXY][Constants.PROXY_USERNAME] != '':
                    self._options['CURLOPT_PROXYUSERPWD'] = '{}:{}'.format(self._config[Constants.PROXY][Constants.PROXY_USERNAME], self._config[Constants.PROXY][Constants.PROXY_PASSWORD])

                if self._config[Constants.PROXY][Constants.PROXY_TYPE] is not None:
                    if self._config[Constants.PROXY][Constants.PROXY_TYPE] == Constants.PROXY_TYPE_HTTP:
                        self._options['CURLOPT_PROXYTYPE'] = "CURLPROXY_HTTP"
                    elif self._config[Constants.PROXY][Constants.PROXY_TYPE] == Constants.PROXY_TYPE_SOCKS5:
                        self._options['CURLOPT_PROXYTYPE'] = "CURLPROXY_SOCKS5"
                    else:
                        raise Exception('Invalid proxy type: {}'.format(self._config[Constants.PROXY][Constants.PROXY_TYPE]))

        if self._config[Constants.BYPASS_SECURE_CONNECTION]:
            self._options['CURLOPT_SSL_VERIFYPEER'] = False
            self._options['CURLOPT_SSL_VERIFYHOST'] = 0
            self._options['CURLOPT_SSLVERSION'] = "CURL_SSLVERSION_DEFAULT"
        else:
            self._options['CURLOPT_SSL_VERIFYPEER'] = True
            self._options['CURLOPT_SSL_VERIFYHOST'] = 2
            self._options['CURLOPT_SSLVERSION'] = "CURL_SSLVERSION_TLSv1_2"

    def _set_composer_options(self):
        """Not used in python"""
        self._composer = {}

    def _evaluate_response(self, response):
        """Evaluates server response

        Args:
            response (dict): Response

        Returns:
            dict: Response

        Raises:
            Exception: If response is invalid"""
        if not isinstance(response, dict):
            raise Exception('Invalid response: must be a dictionary.')

        if 'error' in response and response['error'] is not None:
            raise Exception('Server error: {}'.format(response['error']))
            if not isinstance(response['error'], dict):
                raise Exception('Invalid response: "error" must be a dictionary.')

            if 'code' not in response['error'] or not isinstance(response['error']['code'], int):
                raise Exception('Invalid response: "error" must contain a "code" element.')



        return response['result']

    def raw_request(self, data={}, headers=[]):
        """Performs a raw request

        Args:
            data (dict): JSON-RPC compatible payload
            params (dict): Additional headers as key-value pairs

        Returns:
            dict: Response"""
        for header, value in headers:
            self._options[Constants.CURLOPT_HTTPHEADER][header] = value

        return self._execute(data)

    def _get_last_info(self):
        """Returns the last request information

        Returns:
            dict: Last request information"""
        return self._last_info

    def _get_last_request_headers(self):
        """Returns the HTTP headers of the last request

        Returns:
            dict: HTTP headers"""
        if self._last_info is None:
            return None

        if 'request_header' in self._last_info:
            return self._last_info['request_header']

        return ''

    def _get_last_response_headers(self):
        """Returns the HTTP headers of the last server response

        Returns:
            dict: HTTP headers"""
        return self._last_response_headers


    def get_last_request_content(self):
        """Returns the content of the last request

        This is the last content which was sent as a request. This may be very useful for debugging.

        Returns:
            dict: Last request content"""
        return self._last_request_content

    def get_last_response(self):
        """Returns the last response

        This is the last response which was received from the server. This may be very useful for debugging.

        Returns:
            dict: Last response"""
        return self._last_response

    """Test configuration settings

    Returns:
        bool: True if configuration is valid

    Raises:
        Exception: If configuration is invalid"""
    def _test_config(self):
        """Mandatory settings"""
        mandatory_settings = [
            Constants.URL,
            Constants.KEY
        ]

        for setting in mandatory_settings:
            if setting not in self._config:
                raise Exception(f'Configuration setting "{setting}" is mandatory.')

        """Pre-checks"""
        config = self._config

        """URL"""
        self._check_string(Constants.URL)

        if not self._config[Constants.URL].startswith('http://') and not self._config[Constants.URL].startswith('https://'):
            raise Exception('Unsupported protocol in API URL "{}".'.format(self._config[Constants.URL]))

        """Port"""
        if Constants.PORT in self._config:
            self._check_port(Constants.PORT)
        elif self._config[Constants.URL].startswith('https://'):
            self._config[Constants.PORT] = 443
        elif self._config[Constants.URL].startswith('http://'):
            self._config[Constants.PORT] = 80

        """API key"""
        self._check_string(Constants.KEY)

        """Username and password"""
        if Constants.USERNAME in self._config:
            self._check_string(Constants.USERNAME)

            if not Constants.PASSWORD in self._config:
                raise Exception('Username has no password.')

            self._check_string(Constants.PASSWORD)
        elif Constants.PASSWORD in self._config:
            raise Exception('There is no username.')

        """Language"""
        if Constants.LANGUAGE in self._config:
            self._check_string(Constants.LANGUAGE)

        """Proxy settings"""
        if Constants.PROXY in self._config:
            if not isinstance(self._config[Constants.PROXY], dict):
                raise Exception('Proxy settings must be an object.')

            mandatory_settings = [
                Constants.PROXY_ACTIVE
            ]

            for setting in mandatory_settings:
                if setting not in self._config[Constants.PROXY]:
                    raise Exception(f'Proxy setting "{setting}" is mandatory.')

            """Proxy active"""
            if not isinstance(self._config[Constants.PROXY][Constants.PROXY_ACTIVE], bool):
                raise Exception('Proxy active setting must be a boolean.')

            if self._config[Constants.PROXY][Constants.PROXY_ACTIVE]:
                mandatory_settings = [
                    Constants.PROXY_TYPE,
                    Constants.PROXY_HOST,
                    Constants.PROXY_PORT
                ]

                for setting in mandatory_settings:
                    if setting not in self._config[Constants.PROXY]:
                        raise Exception(f'Proxy setting "{setting}" is mandatory.')

                self._check_string(Constants.PROXY_TYPE, Constants.PROXY)
                self._check_string(Constants.PROXY_HOST, Constants.PROXY)
                self._check_port(Constants.PROXY_PORT, Constants.PROXY)

                if self._config[Constants.PROXY][Constants.PROXY_USERNAME] is not None:
                    self._check_string(Constants.PROXY_USERNAME, Constants.PROXY)

                    if self._config[Constants.PROXY][Constants.PROXY_PASSWORD] is None:
                        raise Exception('Proxy username has no password.')

                    self._check_string(Constants.PROXY_PASSWORD, Constants.PROXY)
                elif self._config[Constants.PROXY][Constants.PROXY_PASSWORD] is not None:
                    raise Exception('There is no proxy username.')

        """Bypass secure connection"""
        if Constants.BYPASS_SECURE_CONNECTION in self._config:
            if not isinstance(self._config[Constants.BYPASS_SECURE_CONNECTION], bool):
                raise Exception('Bypass secure connection setting must be a boolean.')
        else:
            self._config[Constants.BYPASS_SECURE_CONNECTION] = False

        return True

    def _check_string(self, key, sub_key=None):
        """Check if a key is set in configuration and a string"""
        value = None

        if sub_key is not None:
            sub_key = self._config[sub_key][key]
        else:
            value = self._config[key]

        if type(value) is not str:
            raise Exception(f'Configuration setting "{key}" is not a string.')

    def _check_port(self, key, sub_key=None):
        """Checks if a key is a valid port number"""
        value = None

        if sub_key is not None:
            sub_key = self._config[sub_key][key]
        else:
            value = self._config[key]


        if (type(value) is not int) or (value < Constants.PORT_MIN) or (value > Constants.PORT_MAX):
            raise Exception(f'Configuration setting "{key}" is not a valid port number between {Constants.PORT_MIN} and {Constants.PORT_MAX}.')

    def is_logged_in(self):
        """Is client logged-in to API?"""
        return self._session is not None

    def login(self):
        """Login to API"""
        if self.is_logged_in():
            raise Exception('Already logged in')

        """Auto-connect if not connected"""
        if not self.is_connected():
            self.connect()

        response = self.request("idoit.login")

        if response['session-id'] is  None:
            raise Exception('Failed to login because i-doit responded without a session ID')

        self._session = response['session-id']

    def logout(self):
        """Logout from API"""
        if not self.is_logged_in():
            raise Exception('Not logged in')

        self.request("idoit.logout")

        self._session = None

    def _gen_id(self):
        """Generate JSON-RPC request identifier"""
        self._id += 1
        return self._id

    def count_requests(self):
        """How many requests were already send?"""
        return self._id

    def request(self, method, params={}):
        """Sends request to API

        Args:
            method: JSON-RPC method
            params: Optional parameters

        Returns:
            Result of request"""
        data = {
            'version': '2.0',
            'method': method,
            'params': params,
            'id': self._gen_id()
        }

        data["params"]["apikey"] = self._config[Constants.KEY]

        if Constants.LANGUAGE in self._config:
            if Constants.LANGUAGE not in data["params"]:
                data["params"]["language"] = self._config[Constants.LANGUAGE]

        response = self._execute(data)
        self._evaluate_response(response)

        return response['result']

    def batch_request(self, requests):
        """Sends batch request to API

        Args:
            requests: List of requests

        Returns:
            Result of request"""
        data = []

        for request in requests:
            if 'method' not in request:
                raise Exception('Request must have a method')

            params = {}

            if 'params' in request:
                params = request['params']

            params["apikey"] = self._config[Constants.KEY]

            if Constants.LANGUAGE in self._config:
                params["language"] = self._config[Constants.LANGUAGE]

            data.append({
                'version': '2.0',
                'method': request['method'],
                'params': params,
                'id': self._gen_id()
            })

        responses = self._execute(data)

        results = []

        for response in responses:
            if not isinstance(response, dict):
                raise Exception('Response is not a dictionary')
            self._evaluate_response(response)
            results.append(response['result'])

        return results

    def _execute(self, data={}):
        """Sends request to API with headers and receives response"""
        if not self.is_connected():
            self.connect()

        self._last_request_content = data

        data_as_string = json.dumps(data)

        options = self._options

        options["CURLOPT_POSTFIELDS"] = data_as_string

        options["CURLOPT_HTTPHEADER"]["X-RPC-Auth-Username"] = self._config[Constants.USERNAME]
        options["CURLOPT_HTTPHEADER"]["X-RPC-Auth-Password"] = self._config[Constants.PASSWORD]

        #if self._session is not None:
        #    options["CURLOPT_HTTPHEADER"] = {
        #        "X-Auth-Token": self._session
        #    }
        if Constants.USERNAME in self._config and isinstance(self._config[Constants.USERNAME], str) and self._config[Constants.USERNAME] != "" and self._config[Constants.PASSWORD] is not None and isinstance(self._config[Constants.PASSWORD], str) and self._config[Constants.PASSWORD] != "":
            options["CURLOPT_HTTPHEADER"]["X-RPC-Auth-Username"] = self._config[Constants.USERNAME]
            options["CURLOPT_HTTPHEADER"]["X-RPC-Auth-Password"] = self._config[Constants.PASSWORD]

        #curl_setopt_array(self._resource, options)

        headers = options["CURLOPT_HTTPHEADER"]
        payload = options["CURLOPT_POSTFIELDS"]

        s = Session()
        req = ReqRequest("POST", self._config[Constants.URL], data=payload, headers=headers)
        prepped = s.prepare_request(req)
        resp = s.send(prepped)

        resp_body_object = resp.json()

        return resp_body_object

    def is_connected(self):
        """Is client connected to API?"""
        if self._resource is not None:
            return True
        return False

    def connect(self):
        """Connect to API"""
        self._resource = requests.Session()

        if self._resource is None:
            raise Exception('Failed to initialize cURL')

    def disconnect(self):
        if self.is_connected() is False:
            raise Exception('Not connected')

        self._resource = None

    def __del__(self):
        """Destructor"""
        try:
            if self.is_logged_in():
                self.logout()
            if self.is_connected():
                self.disconnect()
        except:
            """Do nothing because this is a destructor."""
            pass


"""Request class for the i-doit API client."""
class Request:
    api = None

    def __init__(self, api):
        """Initialize the request object.

        :param api: The API object
        :type api: API
        """
        self._api = api

    def require_success_for(self, result):
        """Check for success and return identifier.

        :param result: Response from API request
        :type result: dict
        :return: Identifier
        :rtype: int
        """
        if "id" not in result or type(result["id"]) is not int or "success" not in result or type(result["success"]) is not True:
            if "message" in result:
                raise Exception(f"Bad result: {result['message']}")
            else:
                raise Exception("Bad result.")

        return result["id"]

    def require_success_without_identifier(self, result):
        """Check for success but ignore identifier.

        :param result: Response from API request
        :type result: dict
        """
        if "success" not in result or type(result["success"]) is not True:
            if "message" in result:
                raise Exception(f"Bad result: {result['message']}")
            else:
                raise Exception("Bad result.")

    def require_success_for_all(self, results):
        """Check for success for all results.

        :param results: Response from API request
        :type results: list
        """
        for result in results:
            self.require_success_without_identifier(result)
