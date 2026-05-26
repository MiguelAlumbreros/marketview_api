import urllib
import urllib.parse
import urllib.request
import json

from ..results.MvResult import MvResult
from .MvRequests import MvRequests

def symbol_search(self, pattern, env = "prod"):
	parameters = {}

	if pattern is not None:
		escaped_pattern = urllib.parse.quote_plus(pattern)
		parameters['pattern'] = escaped_pattern
	else:
		raise ValueError("Pattern parameter can not be None")

	parameters["env"] = env
 
	request_string = MvRequests.get_request_string("Symbol_Search", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)

def get_symbol_information(self, symbol, ondate = None, info = None, env = "prod"):
	parameters = {}
	
	parameters["symbol"] = self._parse_symbols(symbol)
	if ondate is not None:
		parameters["ondate"] = ondate.strftime('%d-%m-%Y')
	if info is not None:
		parameters["info"] = info
 
	parameters["env"] = env
 
	request_string = MvRequests.get_request_string("Get_Symbol_Information", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)

def get_instrument_list(self, exchangecode = None, optionroot = None, symbol = None, env = "prod"):
	parameters = {}
 
	if exchangecode is not None:
		parameters["exchangecode"] = exchangecode
	if optionroot is not None:
		parameters["optionroot"] = optionroot
	if symbol is not None:
		parameters["symbol"] = self._parse_symbols(symbol)
 
	parameters["env"] = env
 
	request_string = MvRequests.get_request_string("Get_Instrument_List", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)

def delete_symbol(self, symbols, env = "prod"):
	parameters = {}

	data = symbols
	if data is not None:
		json_data = json.dumps(data)
		data = json_data.encode('utf-8')

	parameters['env'] = env

	request_string = MvRequests.get_request_string("Delete_Symbol", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'DELETE',
		data = data	,
		content_type = 'application/json'
	)

	return response

def symbol_search_by_exchange(self, exchangecode, expirationdate=None, securitytype=None, createdate=None, recordsback=None, env="prod"):
	parameters = {
        "output": "csv",
        "env": env,
        "exchangecode": exchangecode
	}

	if expirationdate is not None:
		parameters["expirationdate"] = expirationdate.strftime('%Y-%m-%d')
	if securitytype:
		parameters["securitytype"] = securitytype
	if createdate is not None:
		parameters["createdate"] = createdate.strftime('%Y-%m-%d')
	if recordsback:
		parameters["recordsback"] = recordsback

	request_string = MvRequests.get_request_string("Symbol_Search_By_Exchange", parameters)
	response = self.make_request(
        url=request_string, 
        method='GET',
        data=None,
        content_type='application/json',
        output=False
	)

	return MvResult(response)