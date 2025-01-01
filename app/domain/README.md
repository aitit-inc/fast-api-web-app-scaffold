# Domain Directory

The `domain` directory represents the core of the application’s business logic. This is where the most important concepts, rules, and constraints of the domain are implemented. It contains elements that are independent of specific frameworks or infrastructure, ensuring that the core business logic remains reusable and adaptable.

## Directory Structure

```
domain/
|-- entities/          # Domain entities with unique identifiers
|-- value_objects/     # Value objects representing immutable domain concepts
|-- services/          # Domain services for business logic that doesn’t naturally belong to entities or value objects
|-- repositories/      # Interfaces for accessing domain-related data
|-- factories/         # Factories for creating entities and value objects
```

### `entities/`
This folder contains domain entities, which are objects defined primarily by their unique identity rather than their attributes. Examples include `User`, `Order`, and `Product`. Entities encapsulate the core business rules and maintain the state of the domain.

### `value_objects/`
Here, you define value objects, which represent domain concepts without unique identifiers. They are immutable and often used to model attributes or small groups of attributes, such as `Address`, `Money`, or `Coordinates`.

### `services/`
Domain services encapsulate business logic that cannot naturally fit into an entity or value object. They often represent domain actions or calculations involving multiple entities. For example, a `PaymentService` might handle payment processing rules.

### `repositories/`
This directory includes repository interfaces that define how domain entities are persisted and retrieved. Actual implementations of these interfaces reside in the `infrastructure` layer, ensuring the domain remains independent of specific database or storage technologies.

### `factories/`
Factories are used to create complex entities and value objects. They encapsulate the construction logic, especially when the creation process involves multiple steps or dependencies.

## Principles
1. **Business-Driven Design:** All components in this directory focus solely on the business logic and domain rules.
2. **Framework Independence:** The domain layer should not rely on any external frameworks, libraries, or infrastructure. This ensures its portability and long-term maintainability.
3. **Separation of Concerns:** Entities, value objects, services, repositories, and factories each have distinct responsibilities to promote clarity and reduce coupling.
4. **Testability:** By isolating the domain logic, this layer becomes easier to test independently from external dependencies.

## Guidelines
- Keep the domain layer free from UI, infrastructure, or framework-specific dependencies.
- Ensure that all domain logic and rules are centralized here, rather than dispersed across other layers.
- Use meaningful names for entities and value objects that reflect their role within the domain.
- Avoid including transient or infrastructure-specific logic in domain services.

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
```

**Value Object: `Money`**
```python
class Money:
    def __init__(self, amount: float, currency: str):
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        self.amount = amount
        self.currency = currency

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add amounts with different currencies")
        return Money(self.amount + other.amount, self.currency)
```

## Notes
This structure is flexible and should be adapted to suit the specific needs and complexities of your domain. The goal is to create a maintainable, scalable, and framework-agnostic core for your application.

