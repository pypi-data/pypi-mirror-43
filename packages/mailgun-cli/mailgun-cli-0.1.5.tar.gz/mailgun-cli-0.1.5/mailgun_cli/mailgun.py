import os

from uplink import Consumer, get, Path, Query, params, headers, returns

class Mailgun(Consumer):
    """A Python Client for the GitHub API."""
    def __init__(self):
        super(Mailgun, self).__init__(base_url="https://api.mailgun.net",
                                      auth=('api', os.environ['MAILGUN_API_KEY']))


    # @params( limit=100, skip=0)
    @returns.json
    @get("v3/routes")
    def get_routes(self):
        """Retrieves the user's public repositories."""

if __name__ == '__main__':
    api = Mailgun()
    resp = api.get_routes()
    
    import pprint
    pprint.pprint(resp)
    pass