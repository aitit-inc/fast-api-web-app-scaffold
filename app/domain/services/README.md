# Services Directory

The `services` directory contains domain services, which are responsible for handling domain logic that does not naturally belong to any specific entity or value object. These services encapsulate operations that involve multiple entities or require complex computations.

## Purpose
Domain services:
- Encapsulate business logic that spans multiple entities or aggregates.
- Provide reusable operations that are independent of any particular entity.
- Maintain a clear separation between domain logic and application or infrastructure layers.

## Structure
Each service is typically represented as a class or module, and this directory maintains a flat structure for simplicity:

```
domain/services/
|-- payment_service.py        # Handles payment-related business logic
|-- notification_service.py   # Handles notification-related business logic
|-- ...                       # Additional services
```

## Principles
1. **Business Logic Focus:** Domain services should only contain business logic, not application or infrastructure concerns.
2. **Statelessness:** Whenever possible, keep domain services stateless to simplify their usage and testing.
3. **Reusability:** Design services to be reusable across different parts of the domain or application.

## Guidelines
- Use services to implement business operations that involve multiple entities or complex rules.
- Keep service methods cohesive and focused on specific responsibilities.
- Avoid embedding domain logic into infrastructure or application layers; delegate such operations to domain services.

## Example
**Service: `PaymentService`**
```python
from domain.entities import Order, Payment

class PaymentService:
    @staticmethod
    def calculate_total(order: Order) -> float:
        """Calculate the total amount for an order."""
        return sum(item.price * item.quantity for item in order.items)

    @staticmethod
    def process_payment(order: Order, payment: Payment) -> bool:
        """Validate and process a payment for the given order."""
        total = PaymentService.calculate_total(order)
        if payment.amount < total:
            raise ValueError("Insufficient payment amount")
        # Logic to mark order as paid
        order.mark_as_paid()
        return True
```

**Usage in Domain Layer:**
```python
from domain.services.payment_service import PaymentService
from domain.entities import Order, Payment

order = Order(...)
payment = Payment(amount=100.0)

if PaymentService.process_payment(order, payment):
    print("Payment processed successfully")
```

## Notes
Domain services play a crucial role in maintaining a clean and maintainable architecture by organizing and encapsulating business logic that doesn’t naturally fit within entities or value objects. By centralizing this logic, domain services enhance the clarity, testability, and reusability of the domain layer.

