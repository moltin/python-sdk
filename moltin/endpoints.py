from url import sanitize_url_fragment


class BaseEndpoint():
    # This class is a wrapper around the moltin.request module
    # By subclassing it with a particular endpoint, it provides a more abstracted way to
    # do CRUD operations on that endpoint.
    # E.g.
    #
    # class Product(BaseEndpoint):
    #   def __init__(request):
    #        BaseEndpoint.__init__(request, "product")
    #
    # Usage:
    # product = Product()
    # product.create(params)
    # product.find(5) ## finds by id
    # product.find_by(params) ## finds product that matches given params

    def __init__(self, request, endpoint):
        self.request = request
        self.endpoint = sanitize_url_fragment(endpoint)

    def find(self, id):
        return self.request.get(self.url_with(id))

    def update(self, id, params):
        return self.request.put(self.url_with(id), params=params)

    def remove(self, id):
        return self.request.delete(self.url_with(id))

    def list(self):
        return self.request.get(self.endpoint)

    def find_by(self, params):
        return self.request.get(self.endpoint, params=params)

    def create(self, params):
        return self.request.post(self.endpoint, params=params)

    def url_with(self, param):
        return self.endpoint + "/" + str(param)