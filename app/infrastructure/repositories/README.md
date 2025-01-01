# Repositories Directory

The `repositories` directory contains the concrete implementations of the repository interfaces defined in the domain layer. These implementations handle the actual data access logic and interact with the database or other storage mechanisms.

## Purpose
The purpose of the `repositories` directory is to:
- Bridge the domain layer with the infrastructure layer by implementing repository interfaces.
- Centralize all data access logic to ensure consistency and maintainability.
- Decouple the domain layer from the specific database or storage technologies used.

## Structure
The directory is organized to provide a clear mapping between repository interfaces and their implementations:

```
infrastructure/repositories/
|-- user_repository_impl.py       # Concrete implementation of the UserRepository interface
|-- order_repository_impl.py      # Concrete implementation of the OrderRepository interface
|-- product_repository_impl.py    # Concrete implementation of the ProductRepository interface
```

## Principles
1. **Encapsulation:** Keep data access logic confined to repository implementations.
2. **Consistency:** Ensure that all interactions with the database or storage mechanisms are funneled through repositories.
3. **Adherence to Interface Contracts:** Implement the methods defined in the corresponding domain repository interfaces.

## Guidelines
- Ensure that each repository implementation adheres strictly to its domain-defined interface.
- Use ORM tools (e.g., SQLAlchemy) or raw SQL as appropriate for the project.
- Avoid embedding business logic in repository implementations; they should focus only on data access.
- Implement robust error handling to deal with database or storage-related failures.

## Example
**Domain Interface: `UserRepository`**
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

**Concrete Implementation: `user_repository_impl.py`**
```python
from sqlalchemy.orm import Session
from domain.entities import User
from domain.repositories import UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.session.query(User).filter_by(id=user_id).first()

    def delete(self, user_id: str) -> None:
        user = self.find_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
```

**Usage Example:**
```python
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///example.db")
Session = sessionmaker(bind=engine)
session = Session()

repository = UserRepositoryImpl(session)

# Save a user
user = User(user_id="123", name="John Doe", email="john.doe@example.com")
repository.save(user)

# Retrieve a user
retrieved_user = repository.find_by_id("123")
print(retrieved_user)

# Delete a user
repository.delete("123")
```

## Notes
The `repositories` directory ensures that all database or storage-related operations are encapsulated and centralized. This approach makes the application more maintainable, testable, and adaptable to changes in the underlying storage technology.

