from ..results.MvResult import MvResult
from .MvRequests import MvRequests
from .Structures import RequestBody
import json
import urllib

def get_folder(self, folder, env = "prod"):
	parameters = {}

	if folder is not None:
		# folder = urllib.parse.quote_plus(folder)
		parameters['folder'] = self._parse_symbols(folder)
	else:
		raise ValueError("Folder parameter can not be None")

	parameters['env'] = env

	request_string = MvRequests.get_request_string("Get_Folder", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None	,
		content_type = 'application/json'
	)

	return MvResult(response)

def update_folder(self, body, reason=None, env="prod"):
	parameters = {}
	parameters['env'] = env

	if not isinstance(body, RequestBody):
		raise ValueError("Body parameter must be a RequestBody object")
	
	dict_body = body.to_dict()
	
	# Add reason if provided separately
	if reason is not None:
		dict_body["reason"] = reason
	
	request_data = json.dumps(dict_body).encode('utf-8')

	request_string = MvRequests.get_request_string("Update_Folder", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'PUT',
		data = request_data,
		content_type = 'application/json'
	)

	return MvResult(response)

def delete_folder(self, body, env="prod"):
	parameters = {}
	parameters['env'] = env

	if not isinstance(body, RequestBody):
		raise ValueError("Body parameter must be a RequestBody object")
	
	dict_body = body.to_dict()
	folders = dict_body.get("folders")
	if folders is None:
		raise ValueError("Body must contain 'folders' attribute")
	
	request_data = json.dumps(folders).encode('utf-8')

	request_string = MvRequests.get_request_string("Delete_Folder", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'DELETE',
		data = request_data,
		content_type = 'application/json'
	)

	return response