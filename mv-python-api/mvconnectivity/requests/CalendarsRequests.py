from ..results.MvResult import MvResult
from .MvRequests import MvRequests
import datetime
from .HelperFunctions import filter_list_into_parameter

def get_calendar(self, calendar = None, calendartype = None, env = "prod"):
	parameters = {}

	if calendar is not None:
		parameters['calendar'] = self._filter_list_into_parameter(calendar)

	if calendartype is not None:
		parameters['calendartype'] = calendartype

	parameters['env'] = env

	request_string = MvRequests.get_request_string("Get_Calendar", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)
	return MvResult(response)

def get_calendar_details(self, calendar, startdate = None, enddate = None, tenor = None, quoting = None, env = "prod"):
	parameters = {}

	if calendar is not None:
		parameters['calendar'] = calendar
	else:
		raise ValueError("You must provide calendar parameter")

	if startdate is not None:
		parameters['startdate'] = startdate.strftime('%d-%m-%Y')
		
	if enddate is not None:
		parameters['enddate'] = enddate.strftime('%d-%m-%Y')

	if tenor is not None:
		parameters['tenor'] = self._filter_list_into_parameter(tenor)

	if quoting is not None:
		parameters['quoting'] = quoting

	parameters['env'] = env

	request_string = MvRequests.get_request_string("Get_Calendar_Details", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)

def get_contract_details(self, 
						 rollover, 
						 startdate = None, 
						 enddate = None, 
						 tenor = None, 
						 ondate = None, 
						 env = "prod"):
	parameters = {}
	parameters["env"] = env

	if isinstance(rollover, list):
		if all(isinstance(item, str) for item in rollover):
			parameters["rollover"] = self._filter_list_into_parameter(rollover)
		else:
			raise ValueError("Parameter \"rollover\" must be either string of list of strings.")
	elif isinstance(rollover, str):
		parameters["rollover"] = rollover
	else:
		raise ValueError("Parameter \"rollover\" must be either string of list of strings.")
	
	if startdate is not None and isinstance(startdate, datetime.date):
		parameters["startdate"] = startdate.strftime('%d-%m-%Y')
	elif startdate is not None:
		raise ValueError("Parameter \"start_date\" must be a string.")
	
	if enddate is not None and isinstance(enddate, datetime.date):
		parameters["enddate"] = enddate.strftime('%d-%m-%Y')
	elif enddate is not None:
		raise ValueError("Parameter \"end_date\" must be a string.")
	
	if tenor is not None:
		if isinstance(tenor, list):
			if all(isinstance(item, str) for item in tenor):
				parameters["tenor"] = self._filter_list_into_parameter(tenor)
			else:
				raise ValueError("Parameter \"tenor\" must be either string of list of strings.")
		elif isinstance(tenor, str):
			parameters["tenor"] = tenor
		else:
			raise ValueError("Parameter \"tenor\" must be either string of list of strings.")	

	if ondate is not None and isinstance(ondate, datetime.date):
		parameters["ondate"] = ondate.strftime('%d-%m-%Y')
	elif ondate is not None:
		raise ValueError("Parameter \"on_date\" must be a string.")
	
	request_string = MvRequests.get_request_string("Get_Contract_Details", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

	return MvResult(response)