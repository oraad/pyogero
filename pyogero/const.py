"""constants."""

# from importlib.resources import as_file, files
from typing import NotRequired, TypedDict
from zoneinfo import ZoneInfo

BASEURL = {
    "api": "https://ogero.gov.lb/API",
    "myogero": "https://ogero.gov.lb/myogero",
}

package = "pyogero.resources"
resource = "ogero.pem"

# with as_file(files(package).joinpath(resource)) as file:
#     CERT_PATH = file


DefaultHeaders = TypedDict(
    "DefaultHeaders",
    {
        "Accept": NotRequired[str],
        "Cache-Control": NotRequired[str],
        "Content-Type": NotRequired[str],
        "Origin": NotRequired[str],
        "Referer": NotRequired[str],
    },
)


def default_headers() -> DefaultHeaders:
    """Return a default set of headers."""
    return {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
    }


API_ENDPOINTS = {
    "login": f'{BASEURL["api"]}/Login.php',
    "dashboard": f'{BASEURL["myogero"]}/mobileapp.dashboard.php?SessionID={{session_id}}&Username={{username}}&AppRequest&nbr={{phone_account}}&dsl={{internet_account}}',  # noqa: E501
    "bill": f'{BASEURL["myogero"]}/bill.php?SessionID={{session_id}}&Username={{username}}&AppRequest&nbr={{phone_account}}',  # noqa: E501
    "consumption": f'{BASEURL["myogero"]}/consumption.php?SessionID={{session_id}}&Username={{username}}&AppRequest&dsl={{internet_account}}',  # noqa: E501
}

CONNECTION_SPEED = "Current Bundle"
QUOTA = "Total Quota"
UPLOAD = "Upload"
DOWNLOAD = "Download"
TOTAL_CONSUMPTION = "Total Consumption"
EXTRA_CONSUMPTION = "Extra Consumption"
LAST_UPDATE = "Consumption Until"

LEBANON_TIMEZONE = ZoneInfo("Asia/Beirut")

HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
