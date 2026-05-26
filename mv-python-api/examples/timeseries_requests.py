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

# Sample request | Proprietary curve series (#CH symbol)

mv_result = server_connection.get_curve_timeseries(
    symbol = "#CH.CAT_CS.SYMBOL_CS",
    curvedate = datetime.date(2024, 7, 11),
    fields = ["datetime", "close", "curveroot", "description", "curvedate"],
    env = example_environment
)   
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | Multiple proprietary curve series with start / end dates (#CH symbol)

mv_result = server_connection.get_curve_timeseries(
    symbol = ["#CH.CAT_CS_PROP.SYMBOL_CS","#CH.CAT_CS.SYMBOL_CS"],
    fields = ["datetime","close","curveroot","description","curvedate"],
    curvedate = datetime.date(2024, 7, 11),
    startdate = datetime.date(2023, 11, 11),
    enddate = datetime.date(2024, 7, 14),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | CurveBuilder curve (#DG symbol)

mv_result = server_connection.get_curve_timeseries(
    symbol = "#DG.CAT_DOC.CURVE_DG",
    fields = ["datetime","close","curveroot","description","curvedate"],
    curvedate = datetime.date(2024, 8, 21),
    startdate = datetime.date(2024, 1, 1),
    enddate = datetime.date(2025, 1, 1),
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | Proprietary spot data (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "FIELD", "ONDATE", "INDEX", "VALUE"],
    SYMBOL=["#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP", "#CH.CAT_SP.SYMBOL_SP"],
    FIELD=["CLOSE", "CLOSE", "HIGH", "HIGH"],
    ONDATE=["", "", "", ""],
    INDEX=["2024-03-01T00:00:00Z", "2024-03-02T00:00:00Z", "2024-03-01T00:00:00Z", "2024-03-02T00:00:00Z"],
    VALUE=[14.4, 13.8, 14.3, 13.9]
)
mv_result = server_connection.update_timeseries(
    body=update_body,
    env=example_environment
)

# Sample request body | Proprietary futures data (#CH symbol)

update_body = RequestBody(
    fields=["SYMBOL", "FIELD", "ONDATE", "INDEX", "VALUE"],
    SYMBOL=["#CH.CAT_F.SYMBOL_F/F24", "#CH.CAT_F.SYMBOL_F/F24", "#CH.CAT_F.SYMBOL_F/H24", "#CH.CAT_F.SYMBOL_F/N24", "#CH.CAT_F.SYMBOL_F/Z24"],
    FIELD=["CLOSE", "CLOSE", "CLOSE", "CLOSE", "CLOSE"],
    ONDATE=["", "", "", "", ""],
    INDEX=["2024-01-11T00:00:00Z", "2024-01-12T00:00:00Z", "2024-01-11T00:00:00Z", "2024-01-11T00:00:00Z", "2024-01-11T00:00:00Z"],
    VALUE=[40.8, 40.4, 41.2, 40.4, 50]
)
mv_result = server_connection.update_timeseries(
    body=update_body,
    env=example_environment
)

# Sample request body | Proprietary curve series (#CH symbol)
update_body = RequestBody(
    fields=["SYMBOL", "FIELD", "ONDATE", "INDEX", "VALUE"],
    SYMBOL=["#CH.CAT_CS.SYMBOL_CS", "#CH.CAT_CS.SYMBOL_CS"],
    FIELD=["CLOSE", "CLOSE"],
    ONDATE=["2023-05-05", "2023-05-05"],
    INDEX=["2024-01-30T00:00:00Z", "2024-02-02T00:00:00Z"],
    VALUE=[20.8, 19.7]
)
mv_result = server_connection.update_timeseries(
    body=update_body,
    env=example_environment
)

# Sample request body | CurveBuilder curve (#DG symbol)

update_body = RequestBody(
    fields=["SYMBOL", "FIELD", "ONDATE", "INDEX", "VALUE"],
    SYMBOL=["#DG.CAT_DOC.CURVE_DG", "#DG.CAT_DOC.CURVE_DG", "#DG.CAT_DOC.CURVE_DG"],
    FIELD=["CURVE", "CURVE", "CURVE"],
    ONDATE=["2024-12-05", "2024-12-05", "2024-12-05"],
    INDEX=["2024-11-01T00:00:00Z", "2024-12-01T00:00:00Z", "2025-02-01T00:00:00Z"],
    VALUE=[23.4, 24.2, 26.9]
)
mv_result = server_connection.update_timeseries(
    body=update_body,
    frequency="1M",
    env=example_environment
)

# Sample request body | Proprietary spot data (#CH symbol)

delete_body = RequestBody(
    items=[
        RequestBody(
            symbol="#CH.CAT_SP.SYMBOL_SP",
            field="CLOSE",
            indexes=[
                "2023-07-01T00:00:00Z",
                "2023-08-01T00:00:00Z"
            ]
        ),
        RequestBody(
            symbol="#CH.CAT_SP.SYMBOL_SP",
            field="HIGH",
            indexes=[
                "2023-07-01T00:00:00Z",
                "2023-08-01T00:00:00Z"
            ]
        )
    ]
)
mv_result = server_connection.delete_timeseries(
    body=delete_body,
    env=example_environment
)

# Sample request body | Proprietary futures data (#CH symbol)

delete_body = RequestBody(
    items=[
        RequestBody(
            symbol="#CH.CAT_F.SYMBOL_F/F24",
            field="CLOSE",
            indexes=[
                "2024-01-11T00:00:00Z",
                "2024-01-12T00:00:00Z"
            ]
        ),
        RequestBody(
            symbol="#CH.CAT_F.SYMBOL_F/H24",
            field="CLOSE",
            indexes=[
                "2024-01-11T00:00:00Z"
            ]
        )
    ]
)
mv_result = server_connection.delete_timeseries(
    body=delete_body,
    env=example_environment
)

# Sample request body | Proprietary curve series (#CH symbol)

delete_body = RequestBody(
    items=[
        RequestBody(
            symbol="#CH.CAT_CS.SYMBOL_CS",
            field="CLOSE",
            curvedate="2024-07-11",
            indexes=[
                "2023-11-11T00:00:00Z",
                "2023-11-12T00:00:00Z"
            ]
        )
    ]
)
mv_result = server_connection.delete_timeseries(
    body=delete_body,
    env=example_environment
)