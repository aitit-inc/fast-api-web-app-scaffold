# Interfaces Directory

The `interfaces` directory serves as the bridge between the application and external users or systems. It handles all interactions with external actors, such as clients, APIs, or front-end applications. This layer focuses on user input, output transformation, and request/response handling.

## Directory Structure

```
interfaces/
|-- controllers/       # Controllers for handling incoming requests (REST, GraphQL, etc.)
|-- serializers/       # Serializers for transforming data to and from external formats
|-- views/             # Presentation logic for rendering responses (e.g., HTML, JSON)
```

### `controllers/`
Controllers manage incoming requests and delegate them to the appropriate application layer services. They are responsible for:
- Validating request inputs.
- Invoking application services (use cases).
- Formatting responses to return to the client.

### `serializers/`
Serializers are responsible for transforming data between domain objects and formats suitable for external use, such as JSON or XML. They ensure consistency and standardization of data formats across the application.

### `views/`
This folder contains logic for presenting data to users or external systems. In web applications, it might include:
- HTML templates for rendering pages.
- JSON response handlers for APIs.
- Error pages or success messages.

## Principles
1. **Input/Output Handling:** The `interfaces` layer is solely responsible for managing input and output to ensure that the core application logic remains decoupled from external protocols.
2. **Controller Thinness:** Keep controllers lightweight by delegating complex logic to the application or domain layers.
3. **Consistency:** Use serializers to standardize data formats, reducing potential errors in data representation.

## Guidelines
- Validate all incoming data before passing it to the application layer.
- Use serializers to encapsulate transformation logic and keep controllers clean.
- Ensure that error handling is user-friendly and provides clear feedback to external actors.

## Example
**Controller: `UserController`**

```python
from fastapi import APIRouter, HTTPException
from application.use_cases import RegisterUser
from interfaces.serializers import RegisterUserInputSerializer, RegisterUserOutputSerializer

router = APIRouter()


@router.post("/users/register")
def register_user(request_body: dict):
    input_data = RegisterUserInputSerializer.deserialize(request_body)
    use_case = RegisterUser()
    try:
        result = use_case.__call__(input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return RegisterUserOutputSerializer.serialize(result)
```

**Serializer: `RegisterUserInputSerializer` and `RegisterUserOutputSerializer`**
```python
class RegisterUserInputSerializer:
    @staticmethod
    def deserialize(data: dict):
        return {
            "name": data["name"],
            "email": data["email"],
            "password": data["password"],
        }

class RegisterUserOutputSerializer:
    @staticmethod
    def serialize(data):
        return {
            "id": data.id,
            "email": data.email,
        }
```

## Notes
The `interfaces` directory encapsulates all logic for interacting with external systems and users, ensuring the core logic remains clean and focused on the business domain. By separating concerns in this way, the system becomes more maintainable and testable over time.

