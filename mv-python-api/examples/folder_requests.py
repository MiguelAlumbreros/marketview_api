from mvconnectivity import MvWSConnection
from mvconnectivity.requests.Structures import RequestBody
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

# Sample request |  Proprietary data folders

mv_result = server_connection.get_folder(
    folder = "#CH.COMPANY/DOC_FOLDER",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | All curve dashboard groups

mv_result = server_connection.get_folder(
    folder = "#DG.DASHBOARD",
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | proprietary data folder

update_body = RequestBody(
    folderId = "#CH.COMPANY/DOC_NEW_FOLDER", 
    folders = [RequestBody(name="SUB_FOLDER")],
    content = [RequestBody(symbol="#CH.CAT_SP.SYMBOL_SP")],
    reason = "doc update"
)
mv_result = server_connection.update_folder(
    body = update_body,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request body | curve folder

update_body = RequestBody(
    folderId = "#DG.COMPANY/DOC_CURVEFOLDER",
    folders = [RequestBody(name="SUB1"), RequestBody(name="SUB2")],
    content = [RequestBody(symbol="#DG.CAT_DOC.CURVE_DG")],
    reason = "doc update"
)
mv_result = server_connection.update_folder(
    body = update_body,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | curve group

update_body = RequestBody(
    folderId = "#DG.DASHBOARD/DOC_CURVEGROUP",
    folders = [RequestBody(name="DOC_CURVEGROUP")],
    reason = "doc update"
)
mv_result = server_connection.update_folder(
    body = update_body,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request | add curve to curve dashboard group

update_body = RequestBody(
    folderId = "#DG.DASHBOARD/DOC_CURVEGROUP",
    content = [RequestBody(symbol="#DG.CAT_DOC.CURVE_DG")],
    reason = "doc update"
)
mv_result = server_connection.update_folder(
    body = update_body,
    env = example_environment
)
mv_result = mv_result.to_dataframe()
print(mv_result)

# Sample request

delete_body = RequestBody(
    folders = ["#CH.COMPANY/DOC_FOLDER/SUB_FOLDER1", "#CH.COMPANY/DOC_FOLDER/SUB_FOLDER2"]
)
mv_result = server_connection.delete_folder(
    body = delete_body,
    env = example_environment
)
