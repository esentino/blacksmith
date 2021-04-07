from types import ModuleType
from typing import List

def get_path(module: ModuleType) -> str: ...
def list_module(module: ModuleType) -> List[str]: ...
def find_available_locales(providers: List[str]) -> List[str]: ...
def find_available_providers(modules: List[ModuleType]) -> List[str]: ...
