import urllib
import urllib.parse
import urllib.request
import json
import datetime
import csv
import io
from datetime import datetime, timezone, timedelta

from .MvRequests import MvRequests
from ..results.MvResult import MvResult
from .HelperFunctions import parse_fields, parse_symbols
from .Structures import RequestBody

def get_curve_timeseries(self, symbol, curvedate, fields, startdate = None, enddate = None, timezone = None, env = "prod"):
    parameters = {}

    parameters["env"] = env

    parameters["symbol"] = self._parse_symbols(symbol)
    fields_string, fields, parameters_mapping_user = self._parse_fields(fields)

    if curvedate == "latest":
        parameters["curvedate"] = curvedate
    else:
        parameters["curvedate"] = curvedate.strftime("%m-%d-%Y")
        
    if startdate is not None:
        parameters["startdate"] = startdate.strftime('%Y-%m-%d')
        
    if enddate is not None:
        parameters["enddate"] = enddate.strftime('%Y-%m-%d')

    parameters["fields"] = fields_string
    request_string = MvRequests.get_request_string("Get_Curve_Timeseries", parameters)
    response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

    return MvResult(response, parameters_mapping_user)

def update_timeseries(self, body, frequency=None, env="prod"):
    parameters = {}
    parameters["env"] = env

    if frequency is not None:
        parameters["frequency"] = frequency
        
    if not isinstance(body, RequestBody):
        raise ValueError("Body parameter must be a RequestBody object")
    
    fields, rows = body.to_csv_data()
    
    output_stream = io.StringIO()
    csv_writer = csv.writer(output_stream, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(fields)
    
    for row in rows:
        csv_writer.writerow(row)

    encoded_data = output_stream.getvalue().encode('utf-8')
    output_stream.close()

    request_string = MvRequests.get_request_string("Update_Timeseries", parameters)
    response = self.make_request(
        url=request_string, 
        method='POST',
        data=encoded_data,
        content_type='text/csv',
        output=False
    )

    return response

def delete_timeseries(self, body, env="prod"):
    parameters = {}
    parameters["env"] = env

    if not isinstance(body, RequestBody):
        raise ValueError("Body parameter must be a RequestBody object")
    
    json_data = body.to_dict()
    json_string = json.dumps(json_data).encode('utf-8')

    request_string = MvRequests.get_request_string("Delete_Timeseries", parameters)
    response = self.make_request(
        url=request_string, 
        method='DELETE',
        data=json_string,
        content_type='application/json',
        output=False
    )

    return response
