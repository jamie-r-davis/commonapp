import pytest
import datetime as dt
import os

from config import CAP_USER, CAP_PASSWORD
from commonapp import CommonApp


@pytest.fixture
def cap():
    return CommonApp(CAP_USER, CAP_PASSWORD)

@pytest.fixture
def filename():
    today = dt.datetime.today()
    filename = 'ugaappl_{}.zip'.format(today.strftime('%m%d%Y'))
    yield filename
    try:
        os.remove(filename)
    except:
        pass

def test_login(cap):
    cap.login()

def test_retrieve_file(cap, filename):
    r = cap.retrieve_file(filename)
    assert len(r) > 0

def test_retrieve_file_download(cap, filename):
    f = cap.retrieve_file(filename, local_path=filename)
    assert f == filename
    assert os.path.isfile(filename)
