from bs4 import BeautifulSoup
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

    def list_files(self):
        """
        Retrieve a list of files available via the Control Center.
        """
        url = self.BASE_URL + '/Export/RetrieveFiles'
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tr in soup.select('#retFiles tbody tr'):
            attrs = {}
            keys = ['fileName',
                    'exportTemplateName',
                    'runTime',
                    'processType',
                    'userHeader',
                    'recordsHeader']
            for k in keys:
                v = tr.select_one(f'td[headers={k}]').text.strip()
                attrs[k] = v
            yield attrs


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
        if filename.lower().endswith('.zip'):
            export_type = ''
        uri = '/Export/DownloadFile?fileName={}&type=Export&scheduleType={}'
        url = self.BASE_URL + uri.format(filename, schedule_type)
        self.login()
        stream = self.session.get(url, stream=True)
        if stream.status_code != 200:
            raise Exception(f'{stream.status_code} received.', stream.text)
        if len(stream.content) == 0:
            raise Exception(f'File contains no data: {filename}')
        if local_path:
            with open(local_path, 'wb') as f:
                for chunk in stream.iter_content(chunk_size=1024):
                    f.write(chunk)
            return local_path
        else:
            return response.content
