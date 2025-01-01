# Repositories Directory

The `repositories` directory contains interfaces for managing the persistence and retrieval of domain entities. These interfaces define the contracts for interacting with the data layer without tying the domain logic to specific infrastructure or database technologies.

## Purpose
Repositories:
- Abstract the data access logic to keep the domain layer independent of the underlying database or storage system.
- Define a clear contract for storing and retrieving domain entities.
- Support the Dependency Inversion Principle by allowing infrastructure implementations to fulfill the repository contracts.

## Structure
Each repository interface corresponds to a specific domain entity or aggregate, and this directory maintains a flat structure for simplicity:

```
domain/repositories/
|-- user_repository.py         # Interface for managing User entities
|-- order_repository.py        # Interface for managing Order entities
|-- product_repository.py      # Interface for managing Product entities
|-- ...                        # Additional repositories
```

## Principles
1. **Abstraction:** Repositories abstract the data access logic, allowing the domain layer to remain agnostic of infrastructure details.
2. **Single Responsibility:** Repositories are responsible only for persistence and retrieval, not for implementing domain logic.
3. **Testability:** By defining repository interfaces, the domain layer can be tested independently of the data access implementation.

## Guidelines
- Define repositories as interfaces or abstract classes with methods for common operations like `save`, `find_by_id`, and `delete`.
- Avoid adding domain logic to repository implementations.
- Ensure that repository methods are designed around the domain's needs, not the database schema.

## Example
**Interface: `UserRepository`**
```python
from typing import Protocol, Optional
from domain.entities import User

class UserRepository(Protocol):
    def save(self, user: User) -> None:
        """Persist a User entity."""
        pass

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a User entity by its unique identifier."""
        pass

    def delete(self, user_id: str) -> None:
        """Delete a User entity by its unique identifier."""
        pass
```

**Usage in Domain Layer:**
```python
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user: User) -> None:
        self.user_repository.save(user)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)
```

## Notes
Repositories provide a clear and consistent way to manage the persistence of domain entities while keeping the domain logic decoupled from infrastructure concerns. This approach enhances maintainability, scalability, and testability across the application.

