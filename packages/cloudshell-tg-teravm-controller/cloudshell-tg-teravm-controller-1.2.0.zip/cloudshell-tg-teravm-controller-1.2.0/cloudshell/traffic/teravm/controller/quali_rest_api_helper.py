from requests import packages, Session


packages.urllib3.disable_warnings()


class RestClientException(Exception):
    pass


class RestClientUnauthorizedException(RestClientException):
    pass

# todo: move to separate package

class RestJsonClient(object):

    def __init__(self, hostname, use_https=True):
        super(RestJsonClient, self).__init__()
        self._hostname = hostname
        self._use_https = use_https
        self._session = Session()

    @property
    def session(self):
        return self._session

    def _build_url(self, uri):
        if self._hostname not in uri:
            if not uri.startswith('/'):
                uri = '/' + uri
            if self._use_https:
                url = 'https://{0}{1}'.format(self._hostname, uri)
            else:
                url = 'http://{0}{1}'.format(self._hostname, uri)
        else:
            url = uri
        return url

    def _valid(self, response):
        if response.status_code in [200, 201, 204]:
            return response
        elif response.status_code in [401]:
            raise RestClientUnauthorizedException(self.__class__.__name__, 'Incorrect login or password')
        else:
            raise RestClientException(self.__class__.__name__,
                                      'Request failed: {0}, {1}'.format(response.status_code, response.text))

    def request_put(self, uri, data):
        response = self._session.put(self._build_url(uri), data, verify=False)
        return self._valid(response).json()

    def request_post(self, uri, data):
        response = self._session.post(self._build_url(uri), json=data, verify=False)
        return self._valid(response).json()

    def request_post_files(self, uri, data, files):
        response = self._session.post(self._build_url(uri), data=data, files=files, verify=False)
        return self._valid(response).json()

    def request_get(self, uri):
        response = self._session.get(self._build_url(uri), verify=False)
        return self._valid(response).json()

    def request_get_files(self, uri):
        response = self._session.get(self._build_url(uri), verify=False)
        return self._valid(response)

    def request_delete(self, uri):
        response = self._session.delete(self._build_url(uri), verify=False)
        return self._valid(response).content


def create_quali_api_instance(context, logger):
    """
    Get needed attributes from context and create instance of QualiApiHelper
    :param context: 
    :param logger: 
    :return: 
    """
    if hasattr(context, 'reservation') and context.reservation:
        domain = context.reservation.domain
    elif hasattr(context, 'remote_reservation') and context.remote_reservation:
        domain = context.remote_reservation.domain
    else:
        domain = None
    address = context.connectivity.server_address
    token = context.connectivity.admin_auth_token

    if token:
        instance = QualiAPIHelper(address, logger, token=token, domain=domain)
    else:
        instance = QualiAPIHelper(address, logger, username='admin', password='admin', domain=domain)
    return instance


class QualiAPIHelper(object):
    def __init__(self, server_name, logger, username=None, password=None, token=None, domain=None):
        self._server_name = server_name
        if ":" not in self._server_name:
            self._server_name += ":9000"
        self._domain = domain if domain else None
        self._logger = logger
        self._username = username
        self._password = password
        self._token = token
        self.__rest_client = RestJsonClient(self._server_name, False)

    def upload_file(self, reservation_id, file_stream, file_name):
        # self.remove_attached_files(reservation_id)
        self.attach_new_file(reservation_id, file_stream, file_name)

    def login(self):
        """
        Login
        :return: 
        """
        uri = 'API/Auth/Login'
        if self._token:
            json_data = {'token': self._token, 'domain': self._domain}
        else:
            json_data = {'username': self._username, 'password': self._password, 'domain': self._domain}
        result = self.__rest_client.request_put(uri, json_data)
        self.__rest_client.session.headers.update(authorization="Basic {0}".format(result.replace('"', '')))

    def attach_new_file(self, reservation_id, file_data, file_name):
        file_to_upload = {'QualiPackage': file_data}
        data = {
            "reservationId": reservation_id,
            "saveFileAs": file_name,
            "overwriteIfExists": "true",
        }

        print self.__rest_client.request_post_files('API/Package/AttachFileToReservation',
                                                    data=data,
                                                    files=file_to_upload)

    def get_attached_files(self, reservation_id):
        uri = 'API/Package/GetReservationAttachmentsDetails/{0}'.format(reservation_id)
        result = self.__rest_client.request_get(uri)
        return result['AllAttachments']

    def remove_attached_files(self, reservation_id):
        for file_name in self.get_attached_files(reservation_id):
            file_to_delete = {"reservationId": reservation_id,
                              "FileName": file_name
                              }
            self.__rest_client.request_post('API/Package/DeleteFileFromReservation', data=file_to_delete) or []
