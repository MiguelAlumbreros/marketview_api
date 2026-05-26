from mvconnectivity import MvWSConnection
from mvconnectivity.requests.Structures import TimeSeriesFields, ForwardCurveFields, ForwardCurveValueType, RequestBody
import datetime
from mvconnectivity.requests.Structures import ValueTenor
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

username = os.getenv("MV_USERNAME")
password = os.getenv("MV_PASSWORD")

server_connection = MvWSConnection(username, password)


example_environment = "onboard"

# Sample request | /E.G3BY<1> Futures options

mv_result = server_connection.get_chain(
	optionroot = "/TFN_QUARTER<1>",
	securitytype = "fo",
	fields = ["symbol", "description", "last", "close", "open", "high", "date"],
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | /BRN Futures options with onDate

mv_result = server_connection.get_chain(
    optionroot = "/BRN",
    fields = ["symbol", "tradedatetimeutc", "close", "low"],
    securitytype = "fo",
    ondate = datetime.date(2024, 4, 15),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | MarketView curve

mv_result = server_connection.get_daily_curve(
	symbol = "/GAS",
	curvesize = 4,
	curvedatestart = datetime.date(2024, 6, 1),
	curvedateend = datetime.date(2024, 6, 5),
	fields = ["curveroot", "symbol", "close", "curvedate", "displaydate"],
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol)

mv_result = server_connection.get_daily_curve(
	symbol = "#DG.CAT_DOC.CURVE_DG",
	curvesize = 4,
	curvedatestart = datetime.date(2024, 8, 1),
	curvedateend = datetime.date(2024, 8, 2),
	fields = ["curveroot", "symbol", "close", "curvedate", "displaydate"],
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Proprietary futures data (#CH symbol)

mv_result = server_connection.get_daily_curve(
	symbol = "#CH.CAT_F.SYMBOL_F",
	curvedatestart = datetime.date(2024, 1, 1),
	curvedateend = datetime.date(2024, 8, 21),
	fields = ["curveroot", "symbol", "description", "close", "curvedate", "displaydate"],
	env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample SearchCurves request

search_body = RequestBody(holiday="HUSA")

mv_result = server_connection.search_curves(
	body=search_body,
	env=example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | Proprietary Futures data (#CH symbol)

tenor1 = RequestBody(tenor="F25", value=23.0)
tenor2 = RequestBody(tenor="F26", value=16.0)
tenor3 = RequestBody(tenor="F27", value=19.5)
tenor4 = RequestBody(tenor="F28", value=17.2)

update_body = RequestBody(
    symbol="#CH.CAT_F.FUTURES_SYMBOL",
    onDate=datetime.date(2024, 3, 6),
    tenors=[tenor1, tenor2, tenor3, tenor4],
    field="CLOSE",
    reason="Update"
)

mv_result = server_connection.update_curves(
	body=update_body,
	env=example_environment
)
print(mv_result)

# Sample request body | CurveBuilder curve (#DG symbol)

tenor1 = RequestBody(tenor="M01", value=66.0, relative="M01")
tenor2 = RequestBody(tenor="M02", value=68.0, relative="M02")
tenor3 = RequestBody(tenor="M03", value=67.2, relative="M03")

update_body = RequestBody(
    symbol="#DG.CAT_DOC.CURVE_DG",
    onDate=datetime.date(2024, 3, 1),
    tenors=[tenor1, tenor2, tenor3],
    field="CURVE",
    reason="doc update"
)

mv_result = server_connection.update_curves(
	body=update_body,
	env=example_environment
)
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol) - curve configuration updates

input_obj = RequestBody(
    role="INPUT_B",
    source="MARKETVIEW",
    product="/BRN",
    field="CLOSE",
    offset=0,
    useLastAvailable=False,
    required=True
)

setting_obj = RequestBody(name="DisableBuildForNonQuotingDays", value="1")
property_obj = RequestBody(name="PROP1", value="VALUE4")

build_obj = RequestBody(
    buildType="FormulaPackage",
    runType="Auto",
    buildPriority="-1",
    absolutes="ANY",
    preRulePackage="",
    postRulePackage="",
    shapeName=""
)

update_config_body = RequestBody(
    symbol="#DG.CAT_DOC.CURVE_DG",
    name="CB Curve",
    description="CurveBuilder curve",
    reason="API doc update",
    lotunits="ATM",
    currency="AUD",
    currencyprovider="BOC",
    quotecal="HENG",
    rollcal="REOMBALT",
    decimals="4",
    rounding="UP",
    inputs=[input_obj],
    settings=[setting_obj],
    properties=[property_obj],
    build=build_obj
)

mv_result = server_connection.update_curves(
    body=update_config_body,
    env=example_environment
)
print(mv_result)

# sample request | proprietary futures data (#ch symbol)

mv_result = server_connection.get_table(
    symbol = "#CH.CAT_F.SYMBOL_F",
    fields = ["symbol", "description", "curvedate", "tenor", "absolute", "relative", "expiry", "start", "end", "value", "change", "source", "status", "category", "currency", "units", "code", "company"],
    curvedatestart = datetime.date(2024, 1, 1),
    curvedateend = datetime.date(2024, 5, 15),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol)

mv_result = server_connection.get_table(
    symbol = "#DG.CAT_DOC.CURVE_DG",
    fields = ["symbol", "description", "curvedate", "tenor", "absolute", "relative", "expiry", "start", "end", "value", "change", "source", "status", "category", "currency", "units", "code", "company"],
    curvedatestart = datetime.date(2024, 8, 1),
    curvedateend = datetime.date(2024, 8, 31),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve with curvedate & version (#DG symbol)

mv_result = server_connection.get_table(
    symbol = "#DG.CAT_DOC.CURVE_DG",
    fields = ["symbol", "description", "curvedate", "curveversion", "tenor", "absolute", "relative", "expiry", "start", "end", "value", "change", "source", "status", "category", "currency", "units", "code", "company"],
    curvedate = datetime.date(2024, 8, 1),
    curveversion = "2024-08-27_14:10:13.632",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)
