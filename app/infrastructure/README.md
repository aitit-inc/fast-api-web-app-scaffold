# Infrastructure Directory

The `infrastructure` directory contains implementations and configurations for external systems and services required by the application. It bridges the gap between the application/domain logic and the outside world, handling database connections, API integrations, and other low-level operations.

## Directory Structure

```
infrastructure/
|-- database/           # Database configurations and connections
|-- repositories/       # Concrete implementations of domain repository interfaces
|-- external/           # Integrations with external systems or APIs
|-- config/             # Application configuration files and environment-specific settings
```

### `database/`
This folder contains code and configuration for managing database connections, migrations, and setup. Examples include:
- ORM configurations (e.g., SQLAlchemy, TypeORM)
- Migration scripts (e.g., Alembic, Liquibase)
- Database utilities for connection pooling or custom queries

### `repositories/`
This directory houses concrete implementations of repository interfaces defined in the `domain` layer. These implementations provide the actual logic for data persistence and retrieval, such as:
- SQL queries
- NoSQL database interactions
- File-based storage mechanisms

### `external/`
Code for interacting with external systems, such as:
- API clients (e.g., REST, GraphQL, SOAP)
- Message brokers (e.g., RabbitMQ, Kafka)
- Third-party services (e.g., payment gateways, email providers)

### `config/`
Configuration files and utilities for managing:
- Environment-specific settings (e.g., development, staging, production)
- Application secrets and credentials (e.g., `.env` files, AWS keys)
- Logging and monitoring setups

## Principles
1. **Encapsulation:** Keep infrastructure concerns separate from the domain and application layers.
2. **Framework/Library Abstraction:** Use interfaces or adapters to isolate external dependencies, allowing for easier testing and replacement.
3. **Environment-Agnostic Configurations:** Centralize configuration settings to simplify deployment across different environments.

## Guidelines
- Ensure repository implementations strictly adhere to the interfaces defined in the domain layer.
- Avoid coupling domain logic with infrastructure concerns.
- Use dependency injection to provide infrastructure components to the application layer.
- Validate all external input (e.g., API responses, database queries) before passing it to the application or domain layers.

## Example
**Repository Implementation: `UserRepositoryImpl`**
```python
from domain.repositories import UserRepository
from domain.entities import User

class UserRepositoryImpl(UserRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def save(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()

    def find_by_id(self, user_id: str) -> User:
        return self.db_session.query(User).filter_by(id=user_id).first()
```

**External Service Integration: `PaymentGatewayClient`**
```python
import requests

class PaymentGatewayClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def charge(self, amount: float, currency: str, source: str):
        response = requests.post(f"{self.base_url}/charge", json={
            "amount": amount,
            "currency": currency,
            "source": source,
        }, headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        return response.json()
```

## Notes
The `infrastructure` directory is critical for integrating external dependencies while keeping the domain and application layers clean and focused on core business logic. This separation also makes the application more modular and easier to test.

