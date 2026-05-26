from ..results.MvResult import MvResult
from .MvRequests import MvRequests
import json
import io
import csv

import urllib
import urllib.parse
import urllib.request

from .Structures import TsEnum, TimeSeriesFields, QuoteFields, FillMethod, FillFrequency, AggregateType, ForwardCurveValueType, LeadLagType, ConvertedSymbol, RequestBody
from .ParsingFunctions import _parse_num, _parse_int, _parse_float, _parse_datetime

def get_daily(self, symbols, fields=None, daysback=None, fill=None, maxrows=None, recordsback=None, 
              settledonly=None, startdate=None, enddate=None, aggregatetype=None, currency=None, 
              currencysource=None, lotunits=None, ondate=None, version=None, updatetype=None, 
              lastupdatetime=None, env = "prod"):
    parameters = {}
    
    parameters["symbols"] = self._parse_symbols(symbols)
    
    if fields is not None:
        parameters["fields"], _, _ = self._parse_fields(fields)
    
    if daysback is not None:
        parameters["daysback"] = daysback
    
    if fill in ["forward", "backward", "average", "interpolate", "projected"]:
        parameters["fill"] = fill
    
    if maxrows is not None:
        parameters["maxrows"] = maxrows
    
    if recordsback is not None:
        parameters["recordsback"] = recordsback
    
    if settledonly is not None:
        if settledonly is True:
            parameters["settledonly"] = "true"
    
    if startdate is not None:
        parameters["startdate"] = startdate.strftime('%Y-%m-%d')
    
    if enddate is not None:
        parameters["enddate"] = enddate.strftime('%Y-%m-%d')
    
    if aggregatetype is not None:
        if aggregatetype in [0, 1, 2]:
            parameters["aggregatetype"] = aggregatetype
    
    if currency is not None:
        parameters["currency"] = currency
    
    if currencysource is not None:
        parameters["currencysource"] = currencysource
    
    if lotunits is not None:
        parameters["lotunits"] = lotunits
    
    if ondate is not None:
        parameters["ondate"] = ondate.strftime('%Y-%m-%d')
    
    if version is not None:
        parameters["version"] = version
    
    if updatetype is not None:
        parameters["updatetype"] = updatetype
    
    if lastupdatetime is not None:
        parameters["lastupdatetime"] = lastupdatetime.strftime('%Y-%m-%d')

    parameters["env"] = env
    
    request_string = MvRequests.get_request_string("Get_Daily", parameters)
    response = self.make_request(
        url = request_string, 
        method = 'GET',
        data = None,
        content_type = 'application/json'
    )

    return MvResult(response)

def get_intraday(self, symbols, fields=None, daysback=None, recordsback=None, startdate=None, 
                 enddate=None, aggregatetype=None, currency=None, 
                 currencysource=None, lotunits=None, intradaybarinterval=None, timezone=None, 
                 ondate=None, version=None, updatetype=None, lastupdatetime=None, env = "prod"):
    parameters = {}
    
    parameters["symbols"] = self._parse_symbols(symbols)
    
    if fields is not None:
        parameters["fields"], _, _ = self._parse_fields(fields)
    
    if daysback is not None:
        parameters["daysback"] = daysback
    
    if recordsback is not None:
        parameters["recordsback"] = recordsback
    
    if startdate is not None:
        parameters["startdate"] = startdate.strftime('%Y-%m-%d')
    
    if enddate is not None:
        parameters["enddate"] = enddate.strftime('%Y-%m-%d')
    
    if aggregatetype is not None:
        if aggregatetype in [0, 1, 2]:
            parameters["aggregatetype"] = aggregatetype
    
    if currency is not None:
        parameters["currency"] = currency
    
    if currencysource is not None:
        parameters["currencysource"] = currencysource
    
    if lotunits is not None:
        parameters["lotunits"] = lotunits
    
    if intradaybarinterval is not None:
        parameters["intradaybarinterval"] = intradaybarinterval
        
    if timezone is not None:
        parameters["timezone"] = urllib.parse.quote_plus(timezone)
        
    if ondate is not None:
        parameters["ondate"] = ondate.strftime('%Y-%m-%d')
    
    if version is not None:
        parameters["version"] = version
    
    if updatetype is not None:
        parameters["updatetype"] = updatetype
    
    if lastupdatetime is not None:
        parameters["lastupdatetime"] = lastupdatetime.strftime('%Y-%m-%d')

    parameters["env"] = env
    
    request_string = MvRequests.get_request_string("Get_Intraday", parameters)
    response = self.make_request(
        url = request_string, 
        method = 'GET',
        data = None,
        content_type = 'application/json'
    )

    return MvResult(response)

def get_quote(self, symbols, fields = QuoteFields.ALL, env = "prod"):
    parameters = {}
    if symbols is not None:
        parameters['symbol'] = self._parse_symbols(symbols)
    else:
        raise ValueError("Root(s) missing")

    if fields is not None:
        parameters['fields'], fields, parameters_mapping_user = self._parse_fields(fields)
    else:
        raise ValueError("Fields missing")

    parameters["env"] = env
    
    request_string = MvRequests.get_request_string("Get_Quote", parameters)
    response = self.make_request(
        url = request_string, 
        method = 'GET',
        data = None,
        content_type = 'application/json'
    )

    return MvResult(response)

def update_data(self, body, reason=None, env="prod"):
	parameters = {}
	parameters["env"] = env
	
	if reason is not None:
		parameters["reason"] = reason
	
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
 
	if reason is not None:
		parameters["reason"] = reason

	parameters["env"] = env

	request_string = MvRequests.get_request_string("Update_Data", parameters)
	response = self.make_request(
		url = request_string, 
		method = 'POST',
		data = encoded_data,
		content_type = 'text/csv',
		output = False
	)
	
	return response

def update_data_status(self, correlationId, env = "prod"):
	parameters = {}

	parameters["correlationId"] = correlationId
	parameters["env"] = env

	request_string = MvRequests.get_request_string("Update_Data_Status", parameters)
	response = self.make_request(
		url = request_string,
		method = 'GET',
		data = None,
		content_type = 'text/csv'
	)

	return MvResult(response)

def get_historical_tick(self, symbols, fields = None, daysback = None, env = "prod"):
    parameters = {}
    
    parameters["symbols"] = self._parse_symbols(symbols)
    
    if fields is not None:
        parameters["fields"], fields, parameters_mapping_user = self._parse_fields(fields)
        
    if daysback is not None:
        parameters["daysback"] = daysback
        
    parameters["env"] = env
    
    request_string = MvRequests.get_request_string("Get_Historical_Tick", parameters)
    response = self.make_request(
        url = request_string, 
        method = 'GET',
        data = None,
        content_type = 'application/json'
    )

    return MvResult(response)