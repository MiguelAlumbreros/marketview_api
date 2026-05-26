from mvconnectivity import MvWSConnection
from mvconnectivity.requests.Structures import RequestBody
import datetime
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

# Sample request | MarketView symbols

mv_result = server_connection.get_daily(
    symbols = ["/TFN<0>"],
    fields = ["symbol", "date", "close", "contractdate"],
    # recordsback = 1000,
    startdate = datetime.date(2022, 10, 28),
    enddate = datetime.date(2023, 2, 4),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Corrections

# mv_result = server_connection.get_daily(
#     symbols = "/E.G3BM<0>",
#     fields = ["symbol", "description", "date", "close", "updatetype", "lastupdatetime"],
#     lastupdatetime = datetime.datetime(2023, 1, 26, 15, 0),
#     updatetype = "U",
#     startdate = datetime.date(2023, 1, 26),
#     enddate = datetime.date(2023, 1, 26),
#     env = example_environment
# )
# mv_result = mv_result.to_dataframe()
# print(mv_result)

# Sample request | Corrections 2

mv_result = server_connection.get_daily(
    symbols = "/BRN",
    fields = ["symbol", "description", "date", "close", "updatetype", "lastupdatetime"],
    updatetype = "UI",
    startdate = datetime.date(2024, 2, 1),
    enddate = datetime.date(2024, 2, 13),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Corrections 3

mv_result = server_connection.get_daily(
    symbols = "/BRN",
    fields = ["symbol", "description", "date", "close", "updatetype", "lastupdatetime"],
    lastupdatetime = datetime.datetime(2024, 2, 7, 9, 0),
    updatetype = "UI",
    startdate = datetime.date(2024, 2, 1),
    enddate = datetime.date(2024, 2, 13),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Corrections 4

mv_result = server_connection.get_daily(
    symbols = "/BRN",
    fields = ["symbol", "description", "date", "close", "updatetype", "lastupdatetime"],
    lastupdatetime = datetime.datetime(2024, 2, 7, 9, 0),
    updatetype = "UI",
    daysback = 5,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol) - specifying relative tenor

mv_result = server_connection.get_daily(
    symbols = "#DG.CAT_DOC.CURVE_DG/M02",
    fields = ["symbol", "date", "close"],
    daysback = 20,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol) - specifying absolute tenor

mv_result = server_connection.get_daily(
    symbols = "#DG.CAT_DOC.CURVE_DG/2025M06",
    fields = ["symbol", "date", "close"],
    daysback = 20,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Enverus DataHub data (#EH symbol)

mv_result = server_connection.get_daily(
    symbols = "#EH.EEXFUTREL.EU.EL.DE.EEX.P.Y01",
    fields = ["symbol", "date", "close", "high", "low", "open", "last"],
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | MarketView symbol

mv_result = server_connection.get_historical_tick(
    symbols = "/GNG", 
    fields = ["symbol", "date", "last"], 
    daysback = 1,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | MarketView symbol

mv_result = server_connection.get_intraday(
    symbols = "#CAISO00000053000000014223",
    fields = ["symbol", "date", "description", "open", "high", "low", "close"],
    daysback = 2,
    aggregatetype = 1,
    intradaybarinterval = 60,
    timezone = "publisher",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Corrections

mv_result = server_connection.get_intraday(
    symbols = "#CAISO00000053000000014223",
    fields = ["symbol", "description", "date", "close", "updatetype", "lastupdatetime"],
    startdate = datetime.date(2024, 2, 1),
    enddate = datetime.date(2024, 2, 13),
    lastupdatetime = datetime.datetime(2024, 1, 1, 15, 0),
    updatetype = "U",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | MarketView symbol

mv_result = server_connection.get_quote(
    symbols = "/GCL<*>",
    fields = ["symbol","date","open","high","low","close","volume","sessionstarttimegmt","expirationdate"],
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | Proprietary spot data (#CH symbols)

update_body = RequestBody(
    fields=["SYMBOL", "DATE", "CLOSE"],
    SYMBOL=["#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP"],
    DATE=["01-04-2023", "02-04-2023", "03-04-2023", "04-04-2023"],
    CLOSE=[10.1, 20.2, 30.3, 40.4]
)
mv_result = server_connection.update_data(
    body = update_body,
    reason = "doc_update",
    env = example_environment
)
print(mv_result)

# Sample request | Proprietary spot data with folder specified (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "DATE", "CLOSE", "HIGH", "FOLDER_PATH"],
    SYMBOL=[
        "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP",
        "#CH.CAT_SP.SYMBOL_SP_1", "#CH.CAT_SP.SYMBOL_SP_1", "#CH.CAT_SP.SYMBOL_SP_1", "#CH.CAT_SP.SYMBOL_SP_1"
    ],
    DATE=[
        "01-04-2023", "02-04-2023", "03-04-2023", "04-04-2023", 
        "01-04-2023", "02-04-2023", "03-04-2023", "04-04-2023"
    ],
    CLOSE=[10.1, 20.2, 30.3, 40.4, 50.2, 56.4, 53.9, 50.1],
    HIGH=[10.1, 20.1, 30.1, 40.1, 50.1, 56.1, 53.1, 50.1],
    FOLDER_PATH=[
        "\\DOC_FOLDER\\SPOT", "", "", "", 
        "\\DOC_FOLDER\\SPOT", "", "", ""
    ]
)
mv_result = server_connection.update_data(
    body = update_body,
    reason = "doc_update",
    env = example_environment
)
print(mv_result)

# Sample request | Proprietary spot data with metadata (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "DATE", "CLOSE", "HIGH", "DESCRIPTION", "CURRENCY", "UNIT", "QUOTECAL", "ROLLOVERCAL", "TIMEZONE", "*DENSITY"],
    SYMBOL=["#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP"],
    DATE=["01-04-2023", "02-04-2023", "03-04-2023", "04-04-2023"],
    CLOSE=[10.1, 20.2, 30.3, 40.4],
    HIGH=[10.1, 20.1, 30.1, 40.1],
    DESCRIPTION=["Spot symbol desc", "Spot symbol desc", "Spot symbol desc", "Spot symbol desc"],
    CURRENCY=["USD", "USD", "USD", "USD"],
    UNIT=["BBL", "BBL", "BBL", "BBL"],
    QUOTECAL=["HENG", "HENG", "HENG", "HENG"],
    ROLLOVERCAL=["REOMB", "REOMB", "REOMB", "REOMB"],
    TIMEZONE=["CET", "CET", "CET", "CET"],
    **{"*DENSITY": [45, 45, 45, 45]}
)
mv_result = server_connection.update_data(
    body = update_body,
    reason = "doc_update",
    env = example_environment
)
print(mv_result)

# Sample request | Proprietary futures data with metadata (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "NAME", "DATE", "CLOSE", "CURRENCY", "UNIT", "DESCRIPTION", "QUOTECAL", "ROLLOVERCAL", "TIMEZONE", "SYMBOL_TYPE", "FOLDER_PATH"],
    SYMBOL=["#CH.CAT_F.SYMBOL_F/F24", "#CH.CAT_F.SYMBOL_F/G24", "#CH.CAT_F.SYMBOL_F/H24", "#CH.CAT_F.SYMBOL_F/J24"],
    NAME=["Fut symbol", "Fut symbol", "Fut symbol", "Fut symbol"],
    DATE=["01-04-2023", "01-04-2023", "01-04-2023", "01-04-2023"],
    CLOSE=[10, 20, 30, 40],
    CURRENCY=["CAD", "CAD", "CAD", "CAD"],
    UNIT=["BBL", "BBL", "BBL", "BBL"],
    DESCRIPTION=["Futures symbol", "Futures symbol", "Futures symbol", "Futures symbol"],
    QUOTECAL=["HUSA", "HUSA", "HUSA", "HUSA"],
    ROLLOVERCAL=["REOMB", "REOMB", "REOMB", "REOMB"],
    TIMEZONE=["CET", "CET", "CET", "CET"],
    SYMBOL_TYPE=["F", "F", "F", "F"],
    FOLDER_PATH=["\\DOC_FOLDER\\FUTURES", "", "", ""]
)
mv_result = server_connection.update_data(
    body = update_body,
    reason = "doc_update",
    env = example_environment
)
print(mv_result)

# Sample request | Proprietary forex forward data (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "DATE", "MID", "INDEX", "SYMBOL_TYPE", "FREQUENCY"],
    SYMBOL=["#CH.FXF_YEARLY.FXF_YEARLY/1Y", "#CH.FXF_YEARLY.FXF_YEARLY/ON", "#CH.FXF_YEARLY.FXF_YEARLY/SPOT", "#CH.FXF_YEARLY.FXF_YEARLY/SW", "#CH.FXF_YEARLY.FXF_YEARLY/TN"],
    DATE=["2024-01-01T00:00:00", "2025-01-01T00:00:00", "2026-01-01T00:00:00", "2027-01-01T00:00:00", "2028-01-01T00:00:00"],
    MID=[10, 30, 40, 40, 40],
    INDEX=[1, 3, 4, 8, 12],
    SYMBOL_TYPE=["FXF", "FXF", "FXF", "FXF", "FXF"],
    FREQUENCY=["1Y", "1Y", "1Y", "1Y", "1Y"]
)
mv_result = server_connection.update_data(
    body = update_body,
    reason = "doc_update",
    env = example_environment
)
print(mv_result)

# Sample request body | Proprietary curve series data - monthly frequency (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "DATE", "HIGH", "CURRENCY", "UNIT", "DESCRIPTION", "QUOTECAL", "ROLLOVERCAL", "TIMEZONE", "SYMBOL_TYPE", "FREQUENCY", "VERSION", "CURVEDATE"],
    SYMBOL=["#CH.CAT_CS_MONTHLY.SYMBOL_CS", "#CH.CAT_CS_MONTHLY.SYMBOL_CS", "#CH.CAT_CS_MONTHLY.SYMBOL_CS", "#CH.CAT_CS_MONTHLY.SYMBOL_CS", "#CH.CAT_CS_MONTHLY.SYMBOL_CS"],
    DATE=["2024-01-01T00:00:00", "2024-02-01T00:00:00", "2024-03-01T00:00:00", "2024-04-01T00:00:00", "2024-05-01T00:00:00"],
    HIGH=[4.1, 6.1, 5.2, 3.3, 9.4],
    CURRENCY=["USD", "USD", "USD", "USD", "USD"],
    UNIT=["BRL", "BRL", "BRL", "BRL", "BRL"],
    DESCRIPTION=["TEST", "TEST", "TEST", "TEST", "TEST"],
    QUOTECAL=["HD", "HD", "HD", "HD", "HD"],
    ROLLOVERCAL=["REOMD", "REOMD", "REOMD", "REOMD", "REOMD"],
    TIMEZONE=["UTC", "UTC", "UTC", "UTC", "UTC"],
    SYMBOL_TYPE=["CS", "CS", "CS", "CS", "CS"],
    FREQUENCY=["1M", "1M", "1M", "1M", "1M"],
    VERSION=["FINAL", "FINAL", "FINAL", "FINAL", "FINAL"],
    CURVEDATE=["01-01-2024", "01-01-2024", "02-01-2024", "03-01-2024", "04-01-2024"]
)
mv_result = server_connection.update_data(
    body = update_body,
    reason = "doc_update",
    env = example_environment
)
print(mv_result)

# Sample request

mv_result = server_connection.update_data_status(
    correlationId="f1c8d008-fd08-428f-b567-645d906ef708",
    env = example_environment
)


