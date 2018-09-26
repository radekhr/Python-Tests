import re
from urllib.parse import urljoin

import json
import requests

USERS_API = "https://api.github.com/users/"


class Twitter(object):
    version = '1.0'

    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username

    @property  # do rezultatu funkcji tweets mozemy sie tak samo odwolywac jak wczesniej
    def tweets(self):
        if self.backend and not self._tweets:
            backend_txt = self.backend.read()
            if backend_txt:
                self._tweets = json.loads(backend_txt)
        return self._tweets

    @property
    def tweet_msgs(self):
        return [tweet['msg'] for tweet in self.tweets]

    def get_user_avatar(self):
        if not self.username:
            return None

        url = urljoin(USERS_API, self.username)
        response = requests.get(url)
        return response.json()['avatar_url']

    def tweet(self, msg):
        if len(msg) > 160:
            raise Exception("Message too long!")
        self.tweets.append({'msg': msg, 'avatar': self.get_user_avatar()})
        if self.backend:
            self.backend.write(json.dumps(self.tweets))

    def find_hashtags(self, msg):
        return [m.lower() for m in re.findall("#(\w+)", msg)]

    def get_all_hashtags(self):
        hashtags = []
        for message in self.tweets:
            hashtags.extend(message["hashtags"])
        if hashtags:
            return set(hashtags)
        return "No hashtags found"
