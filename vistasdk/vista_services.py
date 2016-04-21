import settings

# from .base_client import ServiceBase
from vistasdk.base_client import ServiceBase

base_url = {
    "url": settings.VistaService_BASE_URL,
    "protocol": settings.VistaService_BASE_PROTOCOL,
}

service_definitions = settings.service_definitions


class VistaService(ServiceBase):
    def __init__(self, token=None, tld=base_url["url"], protocol=base_url["protocol"], auth_data=None):
        self.token = self._is_logged_in(super(VistaService, self), auth_data)
        if self.token is not None:
            super(VistaService, self).__init__('VistaService', token, tld, protocol)

    def _is_logged_in(self, service, auth_data):
        email = auth_data["email"]
        password = auth_data["password"]
        response = service.authenticate(email=email, password=password)
        is_logged_in, token = service.login(response)
        return token

    # def __init__(self):
    #     super(VistaService, self).__init__('VistaService')

    def get_seatlayout(self,data):
        return self.create("seats", data)

    def get_movies(self):
        return self.list("movies")

    def get_theatres(self):
        return self.list("theatres")

    def get_shows(self):
        return self.list('shows')

    # def describe_movie(self, movie_id):
    #     return self.get("movies", movie_id)
    #
    # def delete_movie(self, movie_id):
    #     return self.delete("movies", movie_id)
    #
    # def update_movie(self, movie_id, data):
    #     return self.update("movies", "{:d}".format(movie_id), data=data)
    #
    #
    # def movie_theatres_by_city(self, movie_id, city):
    #     return self.get("movies", "{:d}/theatres/?city={:s}".format(movie_id, city))



v = VistaService()
# response = v.getseatlayout({
#    "strCinemaCode":"0001MJ",
#    "lngSessionId":18746,
#    "blnScreenOnTop":"false",
#    "strMergeOption":"",
#    "strAreaCatCode":"",
#    "blnExtendedLayout":"false"
# })
response = v.get_movies()
print('layout', response.json())