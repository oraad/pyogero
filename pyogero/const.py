""" constants """
from importlib.resources import files, as_file
from typing import TypedDict
from zoneinfo import ZoneInfo

BASEURL = {
    "api": "https://ogero.gov.lb/API",
    "myogero": "https://ogero.gov.lb/myogero",
}

package = 'pyogero.resources'
resource = 'ogero.pem'

with as_file(files(package).joinpath(resource)) as file:
    CERT_PATH = file


DefaultHeaders = TypedDict(
    "DefaultHeaders",
    {
        "Accept": str,
        "Cache-Control": str,
        "Content-Type": str,
        "Origin": str,
        "Referer": str,
    },
)


def default_headers() -> DefaultHeaders:
    """returns a default set of headers"""
    return {
        "Accept": "application/json",
        # "Content-Type": "application/json",
        # "Origin": "https://ogero.gov.lb",
        # "Referer": "https://ogero.gov.lb/",
        "Cache-Control": "no-cache",
    }


API_ENDPOINTS = {
    "login": f'{BASEURL["api"]}/Login.php',
    "dashboard": f'{BASEURL["myogero"]}/mobileapp.dashboard.php?SessionID={{session_id}}&Username={{username}}&AppRequest&nbr={{phone_account}}&dsl={{internet_account}}',
    "bill": f'{BASEURL["myogero"]}/bill.php?SessionID={{session_id}}&Username={{username}}&AppRequest&nbr={{phone_account}}',
    "consumption": f'{BASEURL["myogero"]}/consumption.php?SessionID={{session_id}}&Username={{username}}&AppRequest&dsl={{internet_account}}',
}

CONNECTION_SPEED = "Current Bundle"
QUOTA = "Total Quota"
UPLOAD = "Upload"
DOWNLOAD = "Download"
TOTAL_CONSUMPTION = "Total Consumption"
EXTRA_CONSUMPTION = "Extra Consumption"
LAST_UPDATE = "Consumption Until"

LEBANON_TIMEZONE = ZoneInfo('Asia/Beirut')