from url import sanitize_url_fragment


class BaseEndpoint():

    def __init__(self, request, endpoint):
        self.request = request
        self.endpoint = sanitize_url_fragment(endpoint)

    def find(self, id):
        return self.request.get(self.url_with(id))

    def update(self, id):
        return self.request.put(self.url_with(id))

    def remove(self, id):
        return self.request.delete(self.url_with(id))

    def list(self):
        return self.request.get(self.endpoint)

    def find_by(self, params):
        return self.request.get(self.endpoint, params)

    def create(self, params):
        return self.request.post(self.endpoint, params)

    def url_with(self, param):
        return self.endpoint + "/" + str(param)