from ..results.MvResult import MvResult
from .MvRequests import MvRequests
from .HelperFunctions import parse_symbols, parse_fields
from .Structures import RequestBody
import json
import io
import csv

def get_metadata(self, symbols, fields = None, include_headers = False, env = "prod"):
	parameters = {}

	if symbols is not None:
		parameters['symbols'] = self._parse_symbols(symbols)
	else:
		raise ValueError("Symbol(s) missing")

	if fields is not None:
		parameters["fields"], fields, parameters_mapping_user = self._parse_fields(fields)

	if include_headers is True:
		parameters["include_headers"] = "true"

	parameters["env"] = env

	request_string = MvRequests.get_request_string("Get_Metadata", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
    )

	if fields is not None:
		parameters_mapping = MvRequests.get_parameters_mapping('Get_Metadata', fields, parameters_mapping_user)
		return MvResult(response, parameters_mapping)
	else:
		return MvResult(response)

def search_metadata(self, body, env="prod"):
    parameters = {}
    
    if not isinstance(body, RequestBody):
        raise ValueError("Body parameter must be a RequestBody object")
    
    json_data = body.to_dict()
    json_string = json.dumps(json_data).encode('utf-8')
 
    parameters["env"] = env

    request_string = MvRequests.get_request_string("Search_Metadata", parameters)
    response = self.make_request(
        url=request_string, 
        method='POST',
        data=json_string,
        content_type='application/json'
    )

    return MvResult(response)

def update_metadata(self, body, env="prod"):
    parameters = {}
    
    if not isinstance(body, RequestBody):
        raise ValueError("Body parameter must be a RequestBody object")
    
    json_data = body.to_dict()
    json_string = json.dumps(json_data).encode('utf-8')

    parameters["env"] = env
    request_string = MvRequests.get_request_string("Update_Metadata", parameters)
    response = self.make_request(
        url=request_string,
        method='PUT',
        data=json_string,
        content_type='application/json'
    )

    return response

def delete_metadata(self, body, env="prod"):
    parameters = {}
    
    if not isinstance(body, RequestBody):
        raise ValueError("Body parameter must be a RequestBody object")
    
    json_data = body.to_dict()
    request_data = json.dumps(json_data).encode('utf-8')
    
    parameters["env"] = env
    
    request_string = MvRequests.get_request_string("Delete_Metadata", parameters)
    response = self.make_request(
        url=request_string, 
        method='DELETE',
        data=request_data,
        content_type='application/json'
    )

    return response
