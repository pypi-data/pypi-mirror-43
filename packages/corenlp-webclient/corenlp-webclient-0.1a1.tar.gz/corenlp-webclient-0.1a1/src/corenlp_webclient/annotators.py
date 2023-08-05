from typing import Any, Dict, Optional, Type

from .options import BaseOptions, WordsToSentenceOptions

__all__ = ['BaseAnnotator', 'WordsToSentenceAnnotator']


class BaseAnnotator:  # pylint:disable=too-few-public-methods
    name: str = ''
    options_class: Type[BaseOptions] = BaseOptions

    def __init__(self, options: Optional[BaseOptions] = None):
        self._options = options

    def make_options_dict(self) -> Dict[str, Any]:
        if not self._options:
            return dict()
        return {'.'.join([self.name, k]): v for k, v in self._options.to_dict().items()}


class WordsToSentenceAnnotator(BaseAnnotator):  # pylint:disable=too-few-public-methods
    name = 'ssplit'
    options_class = WordsToSentenceOptions
