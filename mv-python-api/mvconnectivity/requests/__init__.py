from .MvRequests import MvRequests
from .Structures import TimeseriesParamMapping, DailyCurveParamMapping, QuoteParamMapping

# Curves Requests
MvRequests.add_endpoint("Get_Chain", "getChain")
for key, value in TimeseriesParamMapping.items():
	MvRequests.add_parameter_mapping("Get_Chain", key, value)

MvRequests.add_endpoint("Get_Daily_Curve", "getDailyCurve")
for key, value in TimeseriesParamMapping.items():
	MvRequests.add_parameter_mapping("Get_Daily_Curve", key, value)
for key, value in DailyCurveParamMapping.items():
	MvRequests.add_parameter_mapping("Get_Daily_Curve", key, value)

MvRequests.add_endpoint("Get_Table", "getTable")

MvRequests.add_endpoint("Search_Curves", "searchCurves")

MvRequests.add_endpoint("Get_Daily", "GetDaily")
for key, value in TimeseriesParamMapping.items():
	MvRequests.add_parameter_mapping("Get_Daily", key, value)

MvRequests.add_endpoint("Get_Intraday", "GetIntraday")
for key, value in TimeseriesParamMapping.items():
	MvRequests.add_parameter_mapping("Get_Intraday", key, value)

MvRequests.add_endpoint("Get_Quote", "GetQuote")
for key, value in QuoteParamMapping.items():
	MvRequests.add_parameter_mapping("Get_Quote", key, value)

MvRequests.add_endpoint("Get_Historical_Tick", "getHistoricalTick")

MvRequests.add_endpoint("Symbol_Search", "symbolSearch")
MvRequests.add_endpoint("Get_Symbol_Information", "getSymbolInformation")
MvRequests.add_endpoint("Get_Instrument_List", "getInstrumentList")
MvRequests.add_endpoint("Delete_Symbol", "deleteSymbol")


MvRequests.add_endpoint("Get_Calendar", "getCalendar")
MvRequests.add_endpoint("Get_Calendar_Details", "getCalendarDetails")

MvRequests.add_endpoint("Get_Contract_Details", "getContractDetails")
MvRequests.add_endpoint("Delete_Symbol", "deleteSymbol")

MvRequests.add_endpoint("Get_Folder", "getFolder")
MvRequests.add_endpoint("Update_Folder", "updateFolder")
MvRequests.add_endpoint("Delete_Folder", "deleteFolder")

MvRequests.add_endpoint("Get_Metadata", "getMetadata")
MvRequests.add_endpoint("Search_Metadata", "searchMetadata")
MvRequests.add_endpoint("Update_Metadata", "updateMetadata")
MvRequests.add_endpoint("Delete_Metadata", "deleteMetadata")

MvRequests.add_endpoint("Update_Curves", "updateCurves")
MvRequests.add_endpoint("Update_Data", "updateData")

MvRequests.add_endpoint("Get_Currency_List", "getCurrencyList")
MvRequests.add_endpoint("Get_Exchange_List", "getExchangeList")
MvRequests.add_endpoint("Get_Permissioned_Roots", "getPermissionedRoots")
MvRequests.add_endpoint("Get_Timezones", "getTimezones")
MvRequests.add_endpoint("Get_Unit_List", "getUnitList")
MvRequests.add_endpoint("Symbol_Search_By_Exchange", "symbolSearchByExchange")

MvRequests.add_endpoint("Update_Data_Status", "updateDataStatus")

# Options Requests
MvRequests.add_endpoint("Get_Option_Analytics", "getOptionAnalytics")
MvRequests.add_endpoint("Get_Option_Analytics_Single", "getOptionAnalyticsSingle")

# Timeseries Requests
MvRequests.add_endpoint("Get_Curve_Timeseries", "getCurveTimeSeries")
MvRequests.add_endpoint("Update_Timeseries", "updateTimeseries")
MvRequests.add_endpoint("Delete_Timeseries", "deleteTimeseries")