"""
This module dynamically loads FastAPI routers from submodules and includes them
into a single APIRouter instance.

Key functionality:
- Discovers and imports all submodules using the `pkgutil` library.
- Retrieves the `router` attribute from each module, if present.
- Combines all discovered routers into a single `APIRouter`.

External imports:
- `importlib` for dynamic module imports.
- `pkgutil` for module discovery.
- `APIRouter` from `fastapi` for managing route groups.
"""

import importlib
import pkgutil

from fastapi import APIRouter

# Import the current package (admin) by relative path
# pylint: disable=import-self
from . import __path__ as admin_path

# Initialize the APIRouter
router = APIRouter()

# Dynamically discover and import modules in the admin package
for _, module_name, _ in pkgutil.iter_modules(admin_path):  # type: ignore
    module = importlib.import_module(
        f'.{module_name}', package=__name__)  # Import relatively
    if hasattr(module, 'router'):
        router.include_router(module.router)
