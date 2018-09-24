import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CommonApp:
    """
    CommonApp interface class. Use this class to retrieve information
    from the CommonApp Member Page.
    """

    BASE_URL = 'https://members.commonapp.org'

    def __init__(self, username, password):
        self.session = requests.session()
        self._username = username
        self._password = password

    def login(self):
        """
        Login to the CommonApp.
        """
        url = self.BASE_URL + '/Login'
        data = {'UserName': self._username,
                'Password': self._password}
        response = self.session.post(url, data, verify=False)
        assert response.status_code == 200
        if 'Home Page' in response.text:
            print('Login successful.')
        else:
            raise Exception('Failed to log into CommonApp.')

    def retrieve_file(self, filename, local_path=None):
        """
        Retrive a file from the Control Center.

        If `local_path` is given, the file will be saved to that location,
        otherwise the stream of bytes will be returned.

        Parameters
        ----------
        filename : str
            The filename to retrive.
        local_path : str (optional)
            A local path (dir+filename) where to store the file.
        """
        if filename.lower().startswith('adhoc'):
            schedule_type = 'Adhoc'
        else:
            schedule_type = 'SDS'
        uri = '/Export/DownloadFile?fileName={}&type=Export&scheduleType={}'
        url = self.BASE_URL + uri.format(filename, schedule_type)
        self.login()
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception(f'{r.status_code} received.', response.text)
        if local_path:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
        else:
            return response.content
