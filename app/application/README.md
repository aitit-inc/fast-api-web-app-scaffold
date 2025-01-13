# Application Directory

The `application` directory is responsible for orchestrating the business logic defined in the domain layer. It acts as
the intermediary between the domain and external layers (e.g., interfaces and infrastructure). This layer implements use
cases, defines application-level services, and handles input and output transformations.

## Directory Structure

```
application/
|-- use_cases/          # Application services implementing use cases
|-- dto/                # Data Transfer Objects (DTOs) for input/output transformations
|-- queries/            # Query services for retrieving data without altering the domain state
```

### `use_cases/`

This folder contains application services that implement specific use cases or actions, such as `CreateOrder`,
`UpdateUserProfile`, or `ProcessPayment`. These services coordinate domain logic, manage transactions, and invoke
repository operations as needed.

### `dto/`

Data Transfer Objects are used to structure data between layers. They ensure that external inputs are validated and
transformed into domain-appropriate formats and that domain data is formatted for output to interfaces or external
systems.

### `queries/`

Query services retrieve information from the system without modifying its state. They are often used for reporting or
providing read-only views of the data, ensuring clear separation from domain logic and write operations.

## Principles

1. **Coordination Logic Only:** The application layer does not contain business rules but rather orchestrates their
   execution using the domain layer.
2. **Use Case-Centric Design:** Each use case should correspond to a single, well-defined service.
3. **Isolation of Concerns:** Keep application logic separate from infrastructure and domain logic.
4. **Validation:** Inputs should be validated and transformed into domain models at this layer.

## Guidelines

- Application services should focus on executing a single use case, making them easy to understand and test.
- Avoid embedding domain logic in application services; delegate this responsibility to the domain layer.
- Use DTOs to define clear contracts for input and output data.
- Ensure that query services provide efficient and optimized read operations.

## Example

**Use Case: `RegisterUser`**

```python
from application.dto import RegisterUserInput, RegisterUserOutput
from domain.repositories import UserRepository
from domain.services import UserRegistrationService


class RegisterUser:
    def __init__(self, user_repository: UserRepository, registration_service: UserRegistrationService):
        self.user_repository = user_repository
        self.registration_service = registration_service

    def execute(self, input_data: RegisterUserInput) -> RegisterUserOutput:
        user = self.registration_service.register(
            name=input_data.name,
            email=input_data.email,
            password=input_data.password
        )
        self.user_repository.save(user)
        return RegisterUserOutput(id=user.id, email=user.email)
```

**DTO: `RegisterUserInput` and `RegisterUserOutput`**

```python
class RegisterUserInput:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password


class RegisterUserOutput:
    def __init__(self, id: str, email: str):
        self.id = id
        self.email = email
```

## Notes

The `application` directory bridges the gap between the domain and interface layers, ensuring that business logic is
executed consistently and correctly across different external interactions. Adapt and extend this structure as necessary
to fit the specific requirements of your project.

