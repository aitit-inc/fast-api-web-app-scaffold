# Value Objects Directory

The `value_objects` directory contains immutable objects that represent concepts within the domain. Unlike entities, value objects are defined by their attributes rather than a unique identity. They encapsulate logic related to their value and ensure the integrity and correctness of the domain model.

## Purpose
Value objects:
- Represent domain concepts that are immutable and defined by their values.
- Encapsulate domain logic related to the value, such as validation and operations.
- Ensure consistency and reduce redundancy by reusing common domain concepts.

## Structure
Each value object is typically represented as a class, and this directory maintains a flat structure for simplicity:

```
domain/value_objects/
|-- money.py           # Represents monetary value and currency
|-- address.py         # Represents a postal address
|-- ...                # Additional value objects
```

## Principles
1. **Immutability:** Value objects should be immutable, meaning their state cannot change after creation.
2. **Equality by Value:** Value objects are compared based on their attribute values, not references or identity.
3. **Encapsulation:** Encapsulate logic related to the value within the object itself, such as validation or transformations.

## Guidelines
- Use value objects for concepts that are better defined by their attributes rather than identity.
- Ensure that value objects are immutable by avoiding setter methods and using `@property` for accessors.
- Validate the correctness of values during object creation.
- Provide meaningful methods for operations involving value objects, such as arithmetic or comparisons.

## Example
**Value Object: `Money`**
```python
class Money:
    def __init__(self, amount: float, currency: str):
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        if not currency.isalpha() or len(currency) != 3:
            raise ValueError("Currency must be a valid 3-letter code")

        self._amount = amount
        self._currency = currency

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add amounts with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        return isinstance(other, Money) and self.amount == other.amount and self.currency == other.currency

    def __repr__(self):
        return f"Money(amount={self.amount}, currency='{self.currency}')"
```

**Usage in Domain Layer:**
```python
from domain.value_objects.money import Money

price = Money(amount=50.0, currency="USD")
discount = Money(amount=10.0, currency="USD")

total = price.add(discount)
print(total)  # Output: Money(amount=60.0, currency='USD')
```

## Notes
Value objects enhance the clarity and consistency of the domain model by representing well-defined, immutable concepts. By encapsulating domain logic and ensuring immutability, value objects contribute to a robust and maintainable architecture.

