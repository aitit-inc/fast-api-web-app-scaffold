"""Role and Permission Value Object."""
from enum import Enum


class RoleName(str, Enum):
    """Role name enum."""
    ADMIN = 'admin'
    USER = 'user'


class PermissionName(str, Enum):
    """Permission name enum."""
    ADMIN_READ = 'admin:read'
    ADMIN_WRITE = 'admin:write'
    ADMIN_UPDATE = 'admin:update'
    ADMIN_DELETE = 'admin:delete'
