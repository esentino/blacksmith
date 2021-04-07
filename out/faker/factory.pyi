from typing import Any, Optional

from faker.config import AVAILABLE_LOCALES as AVAILABLE_LOCALES
from faker.config import DEFAULT_LOCALE as DEFAULT_LOCALE
from faker.config import PROVIDERS as PROVIDERS
from faker.generator import Generator as Generator
from faker.utils.loading import list_module as list_module

logger: Any
inREPL: Any

class Factory:
    @classmethod
    def create(
        cls,
        locale: Optional[Any] = ...,
        providers: Optional[Any] = ...,
        generator: Optional[Any] = ...,
        includes: Optional[Any] = ...,
        use_weighting: bool = ...,
        **config: Any,
    ): ...
