from ..results.MvResult import MvResult
from .MvRequests import MvRequests
from .HelperFunctions import filter_list_into_parameter
from .Structures import TimeSeriesFields, ForwardCurveValueType, RequestBody
import io
import csv
import json

def get_chain(self, optionroot, fields = TimeSeriesFields.ALL, securitytype = None, ondate = None, env = "prod"):
	parameters = {}
	parameters["env"] = env

	if optionroot is not None:	
		if isinstance(optionroot, str):
			parameters["optionroot"] = optionroot
		elif isinstance(optionroot, list): 
			parameters["optionroot"] = self._filter_list_into_parameter(optionroot)
		else:
			raise ValueError("Incorrect option_root format")

	if fields is not None:
		parameters["fields"], fields, parameters_mapping_user = self._parse_fields(fields)
	else:
		raise ValueError("Fields missing")

	if securitytype is not None and securitytype not in ["fo", "f"]:
		raise ValueError(f"Security type \"{securitytype}\" not allowed")
	
	if ondate is not None:
		ondate = ondate.strftime('%Y-%m-%d')
		parameters["ondate"] = ondate

	request_string = MvRequests.get_request_string("Get_Chain", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)

def get_daily_curve(self, symbol, fields = TimeSeriesFields.ALL, curvedate = None, curvedatestart = None, curvedateend = None, curvesize = None, curvevaluetype=ForwardCurveValueType.Price, ignoreerrors = None, env = "prod"):
	parameters = {}
	parameters["env"] = env

	if symbol is not None:
		parameters['curveroot'] = self._parse_symbols(symbol)
	else:
		raise ValueError("Root(s) missing")

	if fields is not None:
		parameters['fields'], fields, parameters_mapping_user = self._parse_fields(fields)
	else:
		raise ValueError("Fields missing")

	if curvedate is not None and (curvedatestart is not None and curvedateend is not None):
		raise ValueError("The parameter \"curve_date\" cannot be used together with the curve_date_start and curve_date_end parameters.")

	if curvedate is not None:
		parameters['curvedate'] = curvedate.strftime('%Y/%m/%d')

	if curvedatestart is not None:
		parameters['curvedatestart'] = curvedatestart.strftime('%Y/%m/%d')

	if curvedateend is not None:
		parameters['curvedateend'] = curvedateend.strftime('%Y/%m/%d')

	if curvesize is not None:
		if curvesize <= 0 or not isinstance(curvesize, int):
			raise ValueError("The parameter \"curve_size\" must be a positive integer number.")
		parameters['curvesize'] = curvesize

	if curvevaluetype < ForwardCurveValueType.Price or curvevaluetype > ForwardCurveValueType.SpreadAvg:
		raise ValueError("Invalid curve type")
	else:
		parameters['curvevaluetype'] = curvevaluetype

	if ignoreerrors is not None:
		parameters['ignoreerrors'] = ignoreerrors

	request_string = MvRequests.get_request_string("Get_Daily_Curve", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	parameters_mapping = MvRequests.get_parameters_mapping('Get_Daily_Curve', fields, parameters_mapping_user)
	return MvResult(response, parameters_mapping)

def search_curves(self, body, env = "prod"):
	parameters = {}
	parameters["env"] = env

	if not isinstance(body, RequestBody):
		raise ValueError("Body parameter must be a RequestBody object")
	
	dict_body = body.to_dict()
	json_string = json.dumps(dict_body).encode('utf-8')

	request_string = MvRequests.get_request_string("Search_Curves", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'POST',
		data = json_string,
		content_type = 'application/json',
		output = True
	)
	
	return MvResult(response)

def update_curves(self, body, env="prod"):
	parameters = {}
	parameters["env"] = env

	if not isinstance(body, RequestBody):
		raise ValueError("Body parameter must be a RequestBody object")
	
	dict_body = body.to_dict()
	request_data = json.dumps([dict_body]).encode('utf-8')

	request_string = MvRequests.get_request_string("Update_Curves", parameters)
	response = self.make_request(
		url=request_string, 
		method='POST',
		data=request_data,
		content_type='application/json'
	)

	return response

def get_table(self, symbol, fields, curvedate = None, curvedatestart = None, curvedateend = None, curveversion = None, ignoreerrors = None, env = "prod"):
	parameters = {}
	parameters["env"] = env

	if symbol is not None:
		if isinstance(symbol, str):
			parameters["symbol"] = self._parse_symbols(symbol)
		elif isinstance(symbol, list):
			parameters["symbol"] = self._filter_list_into_parameter(symbol)
		else:
			raise ValueError("Incorrect symbol format")
	else:
		raise ValueError("Symbol(s) missing")

	if fields is not None:
		parameters['fields'], fields, parameters_mapping_user = self._parse_fields(fields)
	else:
		raise ValueError("Fields missing")

	if curvedate is not None:
		if isinstance(curvedate, str) and curvedate.lower() == "latest":
			parameters["curvedate"] = "latest"
		else:
			parameters["curvedate"] = curvedate.strftime('%Y-%m-%d')

	if curvedatestart is not None:
		parameters["curvedatestart"] = curvedatestart.strftime('%Y-%m-%d')

	if curvedateend is not None:
		parameters["curvedateend"] = curvedateend.strftime('%Y-%m-%d')

	if curveversion is not None:
		parameters["curveversion"] = curveversion

	if ignoreerrors is not None:
		parameters["ignoreerrors"] = ignoreerrors

	request_string = MvRequests.get_request_string("Get_Table", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	parameters_mapping = MvRequests.get_parameters_mapping('Get_Table', fields, parameters_mapping_user)
	return MvResult(response, parameters_mapping)