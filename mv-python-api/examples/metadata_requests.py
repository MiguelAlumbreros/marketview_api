from mvconnectivity import MvWSConnection
from mvconnectivity.requests.Structures import RequestBody
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

# Sample request | MarketView symbol

mv_result = server_connection.get_metadata(
    symbols = "/GAS",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Proprietary spot data (#CH symbol)

mv_result = server_connection.get_metadata(
    symbols = "#CH.CAT_SP.SYMBOL_SP",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol)

mv_result = server_connection.get_metadata(
    symbols = "#DG.CAT_DOC.CURVE_DG",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body

search_body = RequestBody(
    COMMODITY = ["COMMODITY TEST"]
)
mv_result = server_connection.search_metadata(
    body = search_body,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | MarketView data, Proprietary spot data (#CH symbol) and CurveBuilder curve (#DG symbol)

update_body = RequestBody(
    items = [
        RequestBody(SYMBOL="/GAS", PROP1="VALUE1"),
        RequestBody(SYMBOL="/GAS", PROP2="VALUE2"),
        RequestBody(SYMBOL="#CH.CAT_SP.SYMBOL_SP", PROP1="VALUE1"),
        RequestBody(SYMBOL="#CH.CAT_SP.SYMBOL_SP", PROP2="VALUE2"),
        RequestBody(SYMBOL="#DG.CAT_DOC.CURVE_DG", PROP1="VALUE1"),
        RequestBody(SYMBOL="#DG.CAT_DOC.CURVE_DG", PROP2="VALUE2")
    ]
)
mv_result = server_connection.update_metadata(
    body = update_body,
    env = example_environment
)

# Sample request body | MarketView data, Proprietary spot data (#CH symbol) and CurveBuilder curve (#DG symbol)

delete_body = RequestBody(
    items = [
        RequestBody(symbol="/GAS", properties=["PROP1", "PROP2"]),
        RequestBody(symbol="#CH.CAT_SP.SYMBOL_SP", properties=["PROP1", "PROP2"]),
        RequestBody(symbol="#DG.CAT_DOC.CURVE_DG", properties=["PROP1", "PROP2"])
    ]
)
mv_result = server_connection.delete_metadata(
    body = delete_body,
    env = example_environment
)