import os

from uplink import Consumer, get, Path, Query, params, headers, returns, post, delete

class Mailgun(Consumer):
    """A Python Client for the Mailgun API."""
    def __init__(self, apikey=None):
        if apikey is None:
            super(Mailgun, self).__init__(base_url="https://api.mailgun.net",
                                      auth=('api', os.environ['MAILGUN_API_KEY']))
        else:
            super(Mailgun, self).__init__(base_url="https://api.mailgun.net",
                                          auth=('api', apikey))


    @returns.json
    @get("v3/routes")
    def list_routes(self, limit: Query("limit")=100, skip: Query("skip")=0):
        """Retrieves the user's public repositories."""

    @post("v3/routes")
    def create_route(self,expression: Query("expression"), action: Query("action"),priority: Query("priority")=0, description: Query(
            "description")=""):
        """create a route"""

    @delete('v3/routes/{id}')
    def delete(self, id):
        """delete a route by id"""

if __name__ == '__main__':
    api = Mailgun()
    resp = api.list_routes(100)
    
    import pprint
    pprint.pprint(resp)
    