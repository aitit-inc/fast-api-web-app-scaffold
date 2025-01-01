"""Error code definitions."""
from enum import Enum


class AppStatusCode(int, Enum):
    """Application-specific status codes.
    
    The six-digit codes are structured as follows:
    - The first two digits identify the category of the status (e.g., 10 for general, 20 for user-related, etc.).
    - The next two digits indicate the specific subcategory if applicable.
    - The last two digits represent the unique status within the category.
    """
    # General codes (10xxxx)
    SUCCESS = 100000  # General success
    FAILURE = 100001  # General failure
    PARTIAL_SUCCESS = 100002  # General partial success

    # User-related codes (20xxxx)
    USER_NOT_FOUND = 200001  # User does not exist
    INVALID_USER_INPUT = 200002  # Invalid input provided by user
    USER_AUTH_FAILURE = 200003  # User authentication failed
    INVALID_REQUEST = 200004 # Invalid request

    # Application-related codes (30xxxx)
    ENTITY_NOT_FOUND = 300001

    # Database-related codes (40xxxx)
    DB_CONNECTION_ERROR = 400001  # Database connection failure
    DB_QUERY_TIMEOUT = 400002  # Database query timed out
    DB_INTEGRITY_ERROR = 400003  # Integrity constraint violation

    # File-handling codes (50xxxx)
    FILE_NOT_FOUND = 500001  # Requested file not found
    FILE_READ_ERROR = 500002  # Error while reading a file
    FILE_WRITE_ERROR = 500003  # Error while writing to a file

    # Service-related codes (60xxxx)
    SERVICE_UNAVAILABLE = 600001  # Dependent service is unavailable
    SERVICE_TIMEOUT = 600002  # Service call timed out
    SERVICE_ERROR = 600003  # Generic service error

    # Placeholder codes for future extensions
    FUTURE_CATEGORY = 700000  # Placeholder for future category codes
