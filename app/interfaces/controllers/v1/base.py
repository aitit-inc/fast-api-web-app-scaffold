"""
This module dynamically loads all FastAPI routers from versioned controller
modules within the `app.interfaces.controllers.v1` package and includes them
into a single FastAPI APIRouter instance (`v1_router`).

Key functionality:
- Imports all modules from the `v1` controllers package
    (`app.interfaces.controllers.v1`) using the `pkgutil` library.
- Checks for the presence of a `router` attribute in each module.
- If the `router` attribute is found, it is included into the `v1_router`
    object.
- Provides a single router object that can be mounted directly into the
    FastAPI app.

External imports:
- `importlib` for dynamically importing modules.
- `pkgutil` for discovering all modules in the `v1` package.
- `APIRouter` from `fastapi` for defining groups of route handlers.

Dependencies:
- The module assumes the `v1` package contains controllers, each optionally
    exposing a `router` object.
"""

import importlib
import pkgutil

from fastapi import APIRouter

from app.interfaces.controllers import v1

v1_router = APIRouter()

for _, module_name, _ in pkgutil.iter_modules(v1.__path__):  # type: ignore
    module = importlib.import_module(
        f'app.interfaces.controllers.v1.{module_name}')
    if hasattr(module, 'router'):
        v1_router.include_router(module.router)
