# Factories Directory

The `factories` directory contains classes and functions responsible for creating instances of domain entities and value objects. Factories encapsulate the construction logic, especially when creating objects involves multiple steps or dependencies.

## Purpose
Factories:
- Centralize complex creation logic for domain entities and value objects.
- Ensure consistency and correctness when creating domain objects.
- Decouple the construction process from the entities themselves, adhering to the Single Responsibility Principle.

## Structure
Each factory is typically represented as a class or function, and this directory maintains a flat structure for simplicity:

```
domain/factories/
|-- user_factory.py        # Factory for creating User entities
|-- order_factory.py       # Factory for creating Order entities
|-- product_factory.py     # Factory for creating Product entities
|-- ...                    # Additional factories
```

## Principles
1. **Encapsulation:** Encapsulate all logic required to create domain objects, including default values and dependencies.
2. **Consistency:** Use factories to ensure that all instances of domain objects are created with valid and consistent data.
3. **Abstraction:** Abstract the creation process to reduce duplication and improve maintainability.

## Guidelines
- Use factories for entities or value objects with complex construction logic.
- Keep factories focused on the creation process without embedding additional domain logic.
- Use dependency injection for any external resources required during the creation process.

## Example
**Factory: `UserFactory`**
```python
from domain.entities import User

class UserFactory:
    @staticmethod
    def create(user_id: str, name: str, email: str) -> User:
        # Additional validation or default assignments can be handled here
        return User(user_id=user_id, name=name, email=email)
```

**Usage:**

```python
from domain.factories.user_factory import UserFactory

# Create a new User entity
user = UserFactory.__call__(user_id="123", name="John Doe", email="john.doe@example.com")
```

## Notes
Factories play a crucial role in maintaining the integrity of the domain model by ensuring that all objects are created in a valid and consistent state. By centralizing creation logic, factories also improve testability and make the codebase easier to maintain.

