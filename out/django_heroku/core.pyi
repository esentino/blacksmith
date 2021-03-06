from typing import Any

from django.test.runner import DiscoverRunner

MAX_CONN_AGE: int
logger: Any

class HerokuDiscoverRunner(DiscoverRunner):
    keepdb: bool = ...
    def setup_databases(self, **kwargs: Any): ...
    def teardown_databases(self, old_config: Any, **kwargs: Any) -> None: ...

def settings(
    config: Any,
    *,
    db_colors: bool = ...,
    databases: bool = ...,
    test_runner: bool = ...,
    staticfiles: bool = ...,
    allowed_hosts: bool = ...,
    logging: bool = ...,
    secret_key: bool = ...,
) -> None: ...
