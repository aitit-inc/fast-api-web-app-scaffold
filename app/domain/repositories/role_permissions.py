"""Roles and Permissions repository interface."""
from abc import ABC

from app.domain.entities.user import Role, Permission
from app.domain.repositories.base import AsyncBaseRepository


class RoleRepository(
    AsyncBaseRepository[int, Role],
    ABC
):
    """Roles repository interface."""


class PermissionRepository(
    AsyncBaseRepository[int, Permission],
    ABC
):
    """Permissions repository interface."""
