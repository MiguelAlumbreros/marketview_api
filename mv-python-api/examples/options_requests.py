from mvconnectivity import MvWSConnection
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

options_fields = ["atmindex", "callput", "symbol", "strike", "mrv", "impvol", "close"]
mv_result = server_connection.get_option_analytics(
    fields = options_fields,
    underlier = "/GCLM25",
    optionmodel = "bs",
    strikecount = 10,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request

options_single_field = ["symbol", "strike", "impvol", "delta", "ghamma", "rho", "theta", "vega"]
mv_result = server_connection.get_option_analytics_single(
    fields = options_single_field,
    symbols = "-GCLM25C15000",
    optionmodel = "bs",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)