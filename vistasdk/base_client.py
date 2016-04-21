import json

import requests

from vistasdk import settings


"""
TODO: prefix (e.g.: /api/v1/) should not be hardcoded
"""
base_url = {
    "url": settings.VistaService_BASE_URL,
    "protocol": settings.VistaService_BASE_PROTOCOL,
}

service_definitions = settings.service_definitions


class ServiceBase(object):
    def __init__(self, service_name, token=None, tld=base_url["url"], protocol=base_url["protocol"]):

        self.token = token
        self.tld = tld
        self.protocol = protocol
        # if token is None:
        # self.token = settings.TOKEN

        self.service_name = service_name
        # self._make_api(service_name)

    def call(self, path, data={}, params=None, method="get"):

        url = self._get_url(path)

        headers = {
            'content-type': 'application/json',
        }
        if self.token is not None:
            headers.update({
                'Authorization': 'Token {0}'.format(self.token)
            })

        http_method = getattr(requests, method)

        return http_method(url, data=json.dumps(data), params=params, headers=headers)

    def authenticate(self, email, password):
        userservice = UserService(tld=self.tld, protocol=self.protocol)
        return userservice.authenticate(email, password)

    def login(self, userservice_response):

        is_logged_in = False

        if userservice_response.status_code == 200:
            self.token = userservice_response.json().get("key")
            is_logged_in = True
        else:
            self.token = None

        return (is_logged_in, self.token)

    def as_json(self, response):
        return json.loads(response.content)

    def info(self, resource):
        '''
        prints information/documentation on a provided resource
        '''
        service_def, resource_def, path = self._get_service_information(
            resource)

        print(resource)
        print("*******************************************")
        print("Base URL: {0}".format(self.tld))
        print("Resource path: {0}".format(resource_def.get("endpoint")))
        print("Required parameters: {0}".format(resource_def.get("required_params")))
        print("Optional parameters".format(resource_def.get("optional_params")))

    def list(self, resource, filter_params=None):
        service_def, resource_def, path = self._get_service_information(
            resource)
        print(path)
        return self.call(path=path, params=filter_params)

    def get(self, resource, resource_id):
        service_def, resource_def, path = self._get_service_information(
            resource)

        get_path = "{0}{1}/".format(path, resource_id)
        return self.call(path=get_path)

    def create(self, resource, data):
        '''
        A base function that performs a default create POST request for a given object
        '''

        service_def, resource_def, path = self._get_service_information(
            resource)
        self._validate(resource, data)

        return self.call(path=path, data=data, method='post')

    def update(self, resource, resource_id, data):
        '''
        A base function that performs a default create PATCH request for a given object
        '''
        service_def, resource_def, path = self._get_service_information(
            resource)

        update_path = "{0}{1}/".format(path, resource_id)
        return self.call(path=update_path, data=data, method='patch')

    def delete(self, resource, resource_id):
        '''
        A base function that performs a default delete DELETE request for a given object
        '''

        service_def, resource_def, path = self._get_service_information(
            resource)
        delete_path = "{0}{1}/".format(path, resource_id)
        return self.call(path=delete_path, method="delete")

    def _make_api(self, service_name):
        '''
        not yet in use ..
        '''

        resources = [resource for resource, resource_details in
                     service_definitions.get(service_name, {}).get("resources", {}).items()]

        for resource in resources:
            setattr(self, 'list_{0}'.format(resource), self.list)
            setattr(self, 'get_{0}'.format(resource), self.get)
            setattr(self, 'create_{0}'.format(resource), self.create)
            setattr(self, 'update_{0}'.format(resource), self.update)
            setattr(self, 'delete_{0}'.format(resource), self.delete)

    def _validate(self, resource, data):

        service_def, resource_def, path = self._get_service_information(
            resource)

        required_params = resource_def.get("required_params", [])
        optional_params = resource_def.get("optional_params", [])

        for param in required_params:
            if data.get(param, None) is None:
                required_params_string = (", ").join(required_params)
                err_message = "{0} is a required parameter for create on {1}. Required parameters are: {2}" \
                    .format(param, resource, required_params_string)
                raise ValueError(err_message)

    def _get_service_information(self, resource):
        service_def = service_definitions.get(self.service_name)
        resource_def = service_def.get("resources", {}).get(resource)
        path = resource_def.get("endpoint")
        return service_def, resource_def, path

    def _get_url(self, path):
        return "{0}{1}".format(self._get_base_url(), path)

    def _get_base_url(self):
        return "{0}://{1}/api/".format(self.protocol, self.tld)

    def _get_headers(self):

        headers = {
            'content-type': 'application/json',
        }

        if self.token is not None:
            headers.update({
                'Authorization': 'Token {0}'.format(self.token)
            })

        return headers


class UserService(ServiceBase):
    def __init__(self, token=None, tld=base_url["url"], protocol=base_url["protocol"]):
        super(UserService, self).__init__('UserService', token, tld, protocol)

    def authenticate(self, username, password):
        data = {
            "email": username,
            "password": password,
        }

        url = "{0}://{1}/api/rest-auth/login/".format(self.protocol, self.tld)

        response = requests.post(url, data)

        return response

    def get_users(self):
        return self.list('user')