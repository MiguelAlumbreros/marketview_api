from mvconnectivity import MvWSConnection
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

server_connection = MvWSConnection(username, password)
example_environment = "onboard"

# Sample GetCurrencyList request

mv_result = server_connection.get_currency_list(env = example_environment)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample GetExchangeList request

mv_result = server_connection.get_exchange_list(env = example_environment)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample GetPermissionedRoots request

fields = ["description", "optionroot", "symbol"]
mv_result = server_connection.get_permissioned_roots(
	fields = fields,
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | All timezones

mv_result = server_connection.get_timezones(
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | WET & UTC timezones & Australia/Canberra ianaCodes

mv_result = server_connection.get_timezones(
	timezones = ["WET","UTC"], 
	ianaCodes = ["Australia/Canberra"],
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample GetUnitList request

mv_result = server_connection.get_unit_list(
    symbol = "/GAS",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)