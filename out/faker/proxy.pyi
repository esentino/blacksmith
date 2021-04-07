from typing import Any, Optional

from faker.config import DEFAULT_LOCALE as DEFAULT_LOCALE
from faker.exceptions import UniquenessException as UniquenessException
from faker.factory import Factory as Factory
from faker.generator import Generator as Generator
from faker.utils.distribution import choices_distribution as choices_distribution

class Faker:
    cache_pattern: Any = ...
    generator_attrs: Any = ...
    def __init__(
        self,
        locale: Optional[Any] = ...,
        providers: Optional[Any] = ...,
        generator: Optional[Any] = ...,
        includes: Optional[Any] = ...,
        use_weighting: bool = ...,
        **config: Any,
    ) -> None: ...
    def __dir__(self): ...
    def __getitem__(self, locale: Any): ...
    def __getattribute__(self, attr: Any): ...
    def __getattr__(self, attr: Any): ...
    @property
    def unique(self): ...
    @classmethod
    def seed(cls, seed: Optional[Any] = ...) -> None: ...
    def seed_instance(self, seed: Optional[Any] = ...) -> None: ...
    def seed_locale(self, locale: Any, seed: Optional[Any] = ...) -> None: ...
    @property
    def random(self): ...
    @random.setter
    def random(self, value: Any) -> None: ...
    @property
    def locales(self): ...
    @property
    def weights(self): ...
    @property
    def factories(self): ...
    def items(self): ...

class UniqueProxy:
    def __init__(self, proxy: Any) -> None: ...
    def clear(self) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
