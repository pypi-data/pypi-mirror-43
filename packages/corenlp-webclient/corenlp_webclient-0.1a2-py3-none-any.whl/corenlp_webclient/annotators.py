from typing import Any, Dict, Type

from .options import BaseOptions, WordsToSentenceOptions

__all__ = ['BaseAnnotator', 'WordsToSentenceAnnotator']


def _snake_to_camel(s):  # type: (str)->str
    parts = s.strip().split('_')
    return parts[0] + ''.join([w.title() for w in parts])


# pylint:disable=too-few-public-methods


class BaseAnnotator:
    name: str = ''
    options_class: Type[BaseOptions] = BaseOptions

    def __init__(self, options: BaseOptions = None):
        self._options = options
        self._options_dict = self.make_options_dict()

    def make_options_dict(self) -> Dict[str, Any]:
        if self._options:
            return {
                '.'.join([self.name, _snake_to_camel(k)]): v
                for k, v in self._options.to_dict().items()
            }
        return {}

    @property
    def options_dict(self) -> Dict[str, Any]:
        return self._options_dict


class WordsToSentenceAnnotator(BaseAnnotator):
    name = 'ssplit'
    options_class = WordsToSentenceOptions
