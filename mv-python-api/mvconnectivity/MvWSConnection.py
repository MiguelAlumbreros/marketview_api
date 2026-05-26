import urllib
from base64 import b64encode

from .DefaultConfig import DefaultConfig

class GvException(Exception):
    def __init__(self, message, inner_exception=None):
        super().__init__(message)
        self.inner_exception = inner_exception

class MvWSConnection:
	def __init__(self, username, password, config = None):
		self._config = config if config is not None else DefaultConfig

		self._version = self._config.VERSION
		self._webservice_url = self._config.WEBSERVICE_URL
		self._api_suffix = self._config.API_SUFFIX
		self._url_base = self._webservice_url + self._api_suffix

		self._response_format = self._config.RESPONSE_FORMAT

		user_pass = f"{username}:{password}"
		self.encoded_credentials = b64encode(user_pass.encode('ascii')).decode('ascii')
		
	@staticmethod
	def register_function(name, function):
		setattr(MvWSConnection, name, function)

	def make_request(self, url, method = 'GET', data = None, content_type = None, output = True):
		try:
			output_string = f"&output={self._response_format}" if output is True else ""
			url = self._url_base + url + output_string
			# print(url)
			headers = {
				'User-Agent': self._version,
				'Content-Type': content_type,
				'Authorization': f"Basic {self.encoded_credentials}"
			}
			request = urllib.request.Request(url, method = method, data = data, headers = headers)
			request_open = urllib.request.urlopen(request)

			response_status_code = request_open.getcode()
			response_text = request_open.read().decode('utf-8')
			# print(f"Response code: {response_status_code}")

			if response_status_code != 200:
				if not response_text:
					response_text = "HTTP error, code: {}".format(response_status_code)

				raise GvException(response_text)

			return response_text

		except Exception as e:
			raise GvException(str(e))