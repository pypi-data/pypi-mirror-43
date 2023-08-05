import requests


class RestClient():
    def __init__(self, myshopify_domain, access_token=None, username=None, password=None):
        self.myshopify_domain = myshopify_domain
        if myshopify_domain is None:
            raise TypeError('myshopify_domain is required')

        self.session = requests.Session()
        if access_token:
            self.session.headers['X-Shopify-Access-Token'] = access_token
        elif username and password:
            self.session.auth = username, password
        else:
            raise ValueError('access_token or username and password are required')

        self.session.headers['Accept'] = 'application/json'

    def _url(self, url):
        return "https://{}/admin/{}".format(self.myshopify_domain, url)

    def get(self, url, **kwargs):
        return self.session.get(self._url(url), **kwargs)

    def put(self, url, **kwargs):
        return self.session.put(self._url(url), **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(self._url(url), **kwargs)

    def patch(self, url, **kwargs):
        return self.session.patch(self._url(url), **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(self._url(url), **kwargs)

    def close(self):
        self.session.close()
