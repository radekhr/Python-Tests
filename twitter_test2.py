from unittest.mock import patch, Mock, MagicMock

import pytest
import requests

from twitter2 import Twitter


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


@pytest.fixture(params=[None, 'python'])
def user_name(request):
    return request.param


@pytest.fixture(params=['tests_list', 'backend'], name='twitter')
def fixture_twitter(backend, user_name, request, monkeypatch):
    if request.param == 'tests_list':
        twitter = Twitter(username=user_name)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=user_name)

    def monkey_return():
        return 'test'

    # monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return)
    return twitter


def test_init_two_twitter_classes(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('test 1')
    twitter2.tweet('test 2')

    assert twitter2.tweet_msgs == ['test 1', 'test 2']


def test_twitter_init(twitter):
    assert twitter


@patch.object(Twitter, 'get_user_avatar', return_value='test')
def test_twitter_single_msg(avatar_mock, twitter):
    # with patch.object(twitter, 'get_user_avatar', return_value='test'):
        twitter.tweet('test msg')
        assert twitter.tweet_msgs == ['test msg']

@pytest.mark.skip
def test_tweet_long_msg(twitter):
    with pytest.raises(Exception):
        twitter.tweet('test' * 50)
    assert twitter.tweets == []


@pytest.mark.parametrize("msg, expected", (
        ("Test #first msg", ["first"]),
        ("#first test msg", ["first"]),
        ("#FIRST test msg", ["first"]),
        ("test msg #first", ["first"]),
        ("test msg #first #second", ["first", "second"]),
))
def test_tweet_with_hashtag(twitter, msg, expected):
    assert twitter.find_hashtags(msg) == expected


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('test message')
    assert twitter.tweets == [{'msg': 'test message', 'avatar': 'test', 'hashtags': []}]
    avatar_mock.assert_called() # sprawdza czy funkcja została wywołana


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hashtags = Mock()
    twitter.find_hashtags.return_value = ['first']
    twitter.tweet("Test #second")
    # assert twitter.tweets[0]['hashtags'] == ['first']
    twitter.find_hashtags.assert_called_with("Test #second")


def test_twitter_version(twitter):
    twitter.version = MagicMock()
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'
