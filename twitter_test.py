import pytest

from twitter import Twitter


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('text.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=['tests_list', 'backend'], name='twitter')
def fixture_twitter(backend, request):
    if request.param == 'tests_list':
        twitter = Twitter()
    elif request.param == 'backend':
        twitter = Twitter(backend=backend)
    return twitter


def test_init_two_twitter_classes(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('test 1')
    twitter2.tweet('test 2')

    assert twitter2.tweet_msgs == ['test 1', 'test 2']


# @pytest.fixture(params=[None, 'text.txt'])
# def twitter(request):
#     twitter = Twitter(backend=request.param)
#     yield twitter # instrukcja ktora tworzy funkcje generujaca
#     twitter.delete()


def test_twitter_init(twitter):
    assert twitter


def test_twitter_single_msg(twitter):
    twitter.tweet('test msg')
    assert twitter.tweet_msgs == ['test msg']


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

