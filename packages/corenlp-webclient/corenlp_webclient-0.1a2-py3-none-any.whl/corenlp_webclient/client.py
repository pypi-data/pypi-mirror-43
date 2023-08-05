import codecs
import json
from typing import Iterable, Union

import requests

from .annotators import BaseAnnotator
from .helpers import backup_emoji, make_properties, restore_emoji, rm_cjk_space

__all__ = ['CoreNlpWebClient']


class CoreNlpWebClient:  # pylint:disable=too-few-public-methods
    DEFAULT_TIMEOUT = 60

    def __init__(self, url: str, session: requests.Session = None, timeout: Union[int, float] = None):
        self._url = url
        self._session = session
        self._timeout = timeout

    def api_call(self, text: str, annotators: Union[Iterable[BaseAnnotator], BaseAnnotator] = None, timeout: Union[int, float] = None):
        text = text.strip()
        text = rm_cjk_space(text)
        text, emoji_map = backup_emoji(text)
        if timeout is None:
            if self._timeout is None:
                timeout = self.DEFAULT_TIMEOUT
            else:
                timeout = self._timeout
        if annotators is None:
            annotators = list()
        elif not isinstance(annotators, Iterable):
            annotators = (annotators,)
        properties = make_properties(*annotators)
        if self._session:
            sender = self._session
        else:
            sender = requests
        response = sender.post(
            self._url,
            params={'properties': json.dumps(properties)},
            data=codecs.encode(text, 'utf-8'),
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
        restore_emoji(data, emoji_map)
        return data
