import json
import logging

import requests

logger = logging.getLogger()


def download_url(url, save_path, chunk_size=1024, parameters=None):
    r = requests.get(url, stream=True, params=parameters)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    logger.info(f'Downloaded "{url}" to "{save_path}"')


def get_json(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Did not get 200 response from query.")
        return False
    jr = json.loads(r.text)
    return jr


###############################################################################
class SessionWithHeaderRedirection(requests.Session):
    """
    overriding requests.Session.rebuild_auth to maintain
    headers when redirected. Pinched off wiki (Aug 2020)
    https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
    """

    AUTH_HOST = "urs.earthdata.nasa.gov"

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from
    # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):

        headers = prepared_request.headers
        url = prepared_request.url

        if "Authorization" in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (
                original_parsed.hostname != redirect_parsed.hostname
                and redirect_parsed.hostname != self.AUTH_HOST
                and original_parsed.hostname != self.AUTH_HOST
            ):
                del headers["Authorization"]
        return None
