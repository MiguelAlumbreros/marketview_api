from ..results.MvResult import MvResult
from .MvRequests import MvRequests
from .HelperFunctions import parse_fields
from .HelperFunctions import filter_list_into_parameter

def get_option_analytics(self,
                         fields, 
                         callput = None, 
                         strikecount = None, 
                         underlier = None, 
                         optionmodel = None,
                         underlierpriceselection = None,
                         contractpriceselection = None,
                         volatility = None,
                         interestrate = None,
                         foreigninterestrate = None,
                         yeardaycount = None,
                         dividendyield = None,
                         env = "prod"):
    parameters = {}
    parameters["env"] = env

    if fields is not None:
        fields_string, fields, parameters_mapping_user = self._parse_fields(fields)
    else:
        raise ValueError("Fields missing")
    
    if callput is not None:
        parameters["callput"] = callput
    if strikecount is not None:
        parameters["strikecount"] = strikecount
    if underlier is not None:
        parameters["underlier"] = underlier
    if optionmodel is not None:
        parameters["optionmodel"] = optionmodel
    if underlierpriceselection is not None:
        parameters["underlierpriceselection"] = underlierpriceselection
    if contractpriceselection is not None:
        parameters["contractpriceselection"] = contractpriceselection
    if volatility is not None:
        parameters["volatility"] = volatility
    if interestrate is not None:
        parameters["interestrate"] = interestrate
    if foreigninterestrate is not None:
        parameters["foreigninterestrate"] = foreigninterestrate
    if yeardaycount is not None:
        parameters["yeardaycount"] = yeardaycount
    if dividendyield is not None:
        parameters["dividendyield"] = dividendyield

    parameters["fields"] = fields_string
    request_string = MvRequests.get_request_string("Get_Option_Analytics", parameters)
    response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

    return MvResult(response, parameters_mapping_user)

def get_option_analytics_single(self,
                         fields, 
                         symbols = None,
                         optionmodel = None,
                         underlierpriceselection = None,
                         contractpriceselection = None,
                         volatility = None,
                         interestrate = None,
                         foreigninterestrate = None,
                         yeardaycount = None,
                         dividendyield = None,
                         env = "prod"):
    parameters = {}
    parameters["env"] = env

    if fields is not None:
        fields_string, fields, parameters_mapping_user = self._parse_fields(fields)
    else:
        raise ValueError("Fields missing")

    if symbols is not None:
        parameters["symbols"] = symbols
    if optionmodel is not None:
        parameters["optionmodel"] = optionmodel
    if underlierpriceselection is not None:
        parameters["underlierpriceselection"] = underlierpriceselection
    if contractpriceselection is not None:
        parameters["contractpriceselection"] = contractpriceselection
    if volatility is not None:
        parameters["volatility"] = volatility
    if interestrate is not None:
        parameters["interestrate"] = interestrate
    if foreigninterestrate is not None:
        parameters["foreigninterestrate"] = foreigninterestrate
    if yeardaycount is not None:
        parameters["yeardaycount"] = yeardaycount
    if dividendyield is not None:
        parameters["dividendyield"] = dividendyield

    parameters["fields"] = fields_string
    request_string = MvRequests.get_request_string("Get_Option_Analytics_Single", parameters)
    response = self.make_request(
		url = request_string, 
		method = 'GET',
		data = None,
		content_type = 'application/json'
	)

    return MvResult(response, parameters_mapping_user)