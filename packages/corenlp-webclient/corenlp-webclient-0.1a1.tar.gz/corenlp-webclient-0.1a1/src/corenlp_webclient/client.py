import codecs
import json
from collections.abc import Iterable
from typing import List, Optional, Union

import requests

from .annotators import BaseAnnotator
from .helpers import backup_emoji, restore_emoji, rm_cjk_space, make_properties

__all__ = ['CoreNlpWebClient']


class CoreNlpWebClient:
    def __init__(self, url: str, session: Optional[requests.Session] = None):
        self._url = url
        self._session = session

    def api_call(self, text: str, annotators: Union[List[BaseAnnotator], BaseAnnotator, None] = None):
        text = text.strip()
        text = rm_cjk_space(text)
        text, emoji_map = backup_emoji(text)
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
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        restore_emoji(data, emoji_map)
        return data
