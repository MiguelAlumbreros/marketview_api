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

# Sample request

mv_result = server_connection.symbol_search(
    pattern = "CAT_CS",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Get by symbol

mv_result = server_connection.get_instrument_list(
    symbol = "#HR",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Get by exchange code

mv_result = server_connection.get_instrument_list(
    exchangecode = "FXE",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Get company marketscript formulas

mv_result = server_connection.get_instrument_list(
    exchangecode = "@company",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | MarketView symbol

mv_result = server_connection.get_symbol_information(
    symbol = "/BRN",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Proprietary spot data symbol (#CH symbol)

mv_result = server_connection.get_symbol_information(
    symbol = "#CH.CAT_SP.SYMBOL_SP",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Curve series

mv_result = server_connection.get_symbol_information(
    symbol = "#CH.CAT_CS.SYMBOL_CS",
    ondate = datetime.date(2024, 7, 11),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Curve series for onDate with versions=info

mv_result = server_connection.get_symbol_information(
    symbol = "#CH.CAT_CS.SYMBOL_CS",
    ondate = datetime.date(2023, 5, 11),
    info = "versions",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol)

mv_result = server_connection.get_symbol_information(
    symbol = "#DG.CAT_DOC.CURVE_DG",
    ondate = datetime.date(2024, 8, 14),
    info = "inputs",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | Proprietary data symbol (#CH symbol)

data = ["#CH.CAT_SP.SYMBOL_SP"]
mv_result = server_connection.delete_symbol(
    symbols = data,
    env = example_environment
)

# Sample request body | CurveBuilder curve (#DG symbol)

data = ["#DG.CAT_DOC.CURVE_DG"]
mv_result = server_connection.delete_symbol(
    symbols = data,
    env = example_environment
)

# Sample request | Argus AUSP exchange code

mv_result = server_connection.symbol_search_by_exchange(
	exchangecode = "AUSP",
	expirationdate = datetime.date(2024, 4, 24),
	securitytype = "SP",
	createdate = datetime.date(2024, 1, 1),
	recordsback = 50000,
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)