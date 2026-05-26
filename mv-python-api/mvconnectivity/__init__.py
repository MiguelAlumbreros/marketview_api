from .MvWSConnection import MvWSConnection
from .requests.HelperFunctions import *
from .requests.AdminRequests import *
from .requests.CalendarsRequests import *
from .requests.CurvesRequests import *
from .requests.DataRequests import *
from .requests.OptionsRequests import *

from .requests.TimeseriesRequests import *
from .requests.SymbolsRequests import *
from .requests.FolderRequests import *
from .requests.MetadataRequests import *

# Helper Functions
MvWSConnection.register_function("_parse_symbols", parse_symbols)
MvWSConnection.register_function("_parse_fields", parse_fields)
MvWSConnection.register_function("_filter_list_into_parameter", filter_list_into_parameter)

# Admin Requests
MvWSConnection.register_function("get_currency_list", get_currency_list)
MvWSConnection.register_function("get_exchange_list", get_exchange_list)
MvWSConnection.register_function("get_permissioned_roots", get_permissioned_roots)
MvWSConnection.register_function("get_timezones", get_timezones)
MvWSConnection.register_function("get_unit_list", get_unit_list)

# Calendars Requests
MvWSConnection.register_function("get_calendar", get_calendar)
MvWSConnection.register_function("get_calendar_details", get_calendar_details)

# Contracts Requests
MvWSConnection.register_function("get_contract_details", get_contract_details)

# Curves Requests
MvWSConnection.register_function("get_chain", get_chain)
MvWSConnection.register_function("get_daily_curve", get_daily_curve)
MvWSConnection.register_function("search_curves", search_curves)
MvWSConnection.register_function("update_curves", update_curves)
MvWSConnection.register_function("get_table", get_table)

# Data Requests

MvWSConnection.register_function("update_data", update_data)
MvWSConnection.register_function("update_data_status", update_data_status)

MvWSConnection.register_function("get_daily", get_daily)
MvWSConnection.register_function("get_historical_tick", get_historical_tick)
MvWSConnection.register_function("get_intraday", get_intraday)
MvWSConnection.register_function("get_quote", get_quote)

MvWSConnection.register_function("symbol_search", symbol_search)
MvWSConnection.register_function("get_instrument_list", get_instrument_list)
MvWSConnection.register_function("delete_symbol", delete_symbol)
MvWSConnection.register_function("get_symbol_information", get_symbol_information)
MvWSConnection.register_function("symbol_search_by_exchange", symbol_search_by_exchange)

MvWSConnection.register_function("get_folder", get_folder)
MvWSConnection.register_function("update_folder", update_folder)
MvWSConnection.register_function("delete_folder", delete_folder)

MvWSConnection.register_function("get_metadata", get_metadata)
MvWSConnection.register_function("search_metadata", search_metadata)
MvWSConnection.register_function("update_metadata", update_metadata)
MvWSConnection.register_function("delete_metadata", delete_metadata)

MvWSConnection.register_function("update_curves", update_curves)
MvWSConnection.register_function("update_data", update_data)

# Options Requests
MvWSConnection.register_function("get_option_analytics", get_option_analytics)
MvWSConnection.register_function("get_option_analytics_single", get_option_analytics_single)

# Timeseries Requests
MvWSConnection.register_function("get_curve_timeseries", get_curve_timeseries)
MvWSConnection.register_function("update_timeseries", update_timeseries)
MvWSConnection.register_function("delete_timeseries", delete_timeseries)
