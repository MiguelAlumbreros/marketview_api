from ..results.MvResult import MvResult
from .MvRequests import MvRequests
from .HelperFunctions import parse_fields
from .HelperFunctions import filter_list_into_parameter


def get_currency_list(self, env = "prod"):
	parameters = {}
	parameters["output"] = "csv"
	parameters["env"] = env

	request_string = MvRequests.get_request_string("Get_Currency_List", parameters)
	response = self.make_request(
		url = request_string,
		method = 'GET',
		data = None,
		content_type = 'application/json',
		output = False
	)

	return MvResult(response)

def get_exchange_list(self, env = "prod"):
	parameters = {}
	parameters["output"] = "csv"
	parameters["env"] = env

	request_string = MvRequests.get_request_string("Get_Exchange_List", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json',
		output = False
	)

	return MvResult(response)

def get_permissioned_roots(self, fields, env = "prod"):
	parameters = {}
	parameters["env"] = env
	
	if fields is not None:
		fields_string, fields, parameters_mapping_user = self._parse_fields(fields)
	else:
		raise ValueError("Fields missing")

	parameters["fields"] = fields_string
	request_string = MvRequests.get_request_string("Get_Permissioned_Roots", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response, parameters_mapping_user)

def get_timezones(self, timezones = None, ianaCodes = None, env = "prod"):
	parameters = {}

	parameters["env"] = env
	if timezones is not None:
		parameters["timezones"] = self._filter_list_into_parameter(timezones)
	if ianaCodes is not None:
		parameters["ianaCodes"] = self._filter_list_into_parameter(ianaCodes)

	request_string = MvRequests.get_request_string("Get_Timezones", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)

def get_unit_list(self, symbol, env = "prod"):
	parameters = {}
	parameters["output"] = "csv"

	if symbol is not None and isinstance(symbol, str):
		parameters["symbol"] = symbol
	elif symbol is not None:
		raise ValueError("Parameter \"symbol\" must be a string.")
	else:
		raise ValueError("Parameter \"symbol\" must be included.")

	parameters["env"] = env

	request_string = MvRequests.get_request_string("Get_Unit_List", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json',
		output = False
	)

	return MvResult(response)
