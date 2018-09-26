import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')  # wylaczenie z działania atrybutu


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('text.txt')
    temp_file.write('')
    return temp_file