# Entities Directory

The `entities` directory contains the core domain objects that are primarily defined by their unique identities. Entities encapsulate the business logic and maintain the state of the application domain. They represent the most fundamental and consistent concepts within the domain model.

## Purpose
Entities:
- Represent objects with a unique identifier that distinguishes them from others.
- Contain attributes and behaviors that are intrinsic to the domain logic.
- Act as the backbone of the domain layer by encapsulating business rules and state changes.

## Structure
Each entity is typically represented as a class, and this directory maintains a flat structure for simplicity:

```
domain/entities/
|-- user.py           # User entity
|-- order.py          # Order entity
|-- product.py        # Product entity
|-- ...               # Additional entities
```

## Principles
1. **Identity:** Each entity must have a unique identifier (e.g., `id` or `uuid`) that persists across its lifecycle.
2. **Business Logic:** Encapsulate the rules and behaviors that define the entity's role in the domain.
3. **Consistency:** Ensure state changes adhere to the business rules and constraints of the domain.

## Guidelines
- Keep entity logic focused on domain-specific responsibilities.
- Use methods to enforce invariants and encapsulate behaviors.
- Avoid direct dependencies on external systems (e.g., databases, APIs).
- Ensure attributes and methods are meaningful and relevant to the entity's purpose.

## Example
**Entity: `User`**
```python
class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def change_email(self, new_email: str):
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email format")
        self.email = new_email

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Simplified email validation logic
        return "@" in email

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, email={self.email})"
```

## Notes
Entities are central to the domain layer and should reflect the core concepts of your application. By keeping entities focused and cohesive, you ensure that the domain model remains robust and maintainable.

