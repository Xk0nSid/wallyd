import requests
from wally.provider import Provider, BaseProvider


@Provider.register
class Unsplash(BaseProvider):

    def __init__(self, config):
        self.api_base_url = config['api_base_url'].rstrip('/')
        self.access_key = config['access_key']
        self.mode = config['mode']
        self.search_term = config['search_term']
        self.pagination = config['pagination']
        self.wallpapers = []
        self.ix = 0
        self.page = 0

        if self.mode == "search":
            self.endpoint = "search/photos"
        else:
            self.endpoint = "photos/random"

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.wallpapers) <= 0:
            self._populate(self._api_request())
        if self.ix == len(self.wallpapers) - 1:
            self.ix = 0
            self.page += 1
            self._populate(self._api_request())
        else:
            self.ix += 1
        return self.wallpapers[self.ix]

    def _api_request(self):
        url = self._build_url()
        payload = self._build_payload()
        resp = requests.get(url, params=payload)
        data = resp.json()
        return data

    def _build_payload(self):
        payload = {
            'client_id': self.access_key,
            'page': self.page,
            'per_page': self.pagination,
        }
        if self.mode == "search":
            payload['query'] = self.search_term
        return payload

    def _build_url(self):
        return "{}/{}".format(self.api_base_url, self.endpoint)

    def _populate(self, data):
        """
        Go through the response from api and push the appropriate
        url of wallpaper in instance array
        """
        pass
