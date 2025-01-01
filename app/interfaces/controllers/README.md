# Controllers Directory

The `controllers` directory contains classes or modules responsible for handling incoming requests and delegating them to the appropriate application layer services. Controllers serve as the entry point for user interactions, APIs, or external systems, ensuring that input is processed and responses are returned in the correct format.

## Purpose
The purpose of the `controllers` directory is to:
- Manage HTTP or other protocol-specific requests.
- Validate and process input before passing it to the application layer.
- Format and return responses to the client in a standardized way.

## Structure
The directory organizes controllers by feature or module, keeping them manageable and cohesive:

```
interfaces/controllers/
|-- user_controller.py        # Handles user-related requests
|-- order_controller.py       # Handles order-related requests
|-- product_controller.py     # Handles product-related requests
```

## Principles
1. **Thin Controllers:** Keep controllers focused on request handling and delegate business logic to the application layer.
2. **Input Validation:** Validate and sanitize incoming data to ensure correctness and security.
3. **Consistent Responses:** Standardize the format of responses for a better client experience.

## Guidelines
- Use controllers as the primary interaction point for external systems.
- Perform input validation using serializers or validation libraries.
- Handle errors gracefully and return meaningful HTTP status codes and messages.
- Avoid embedding business logic directly in controllers; use application services instead.

## Example
**Controller: `user_controller.py`**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from application.use_cases import RegisterUser

router = APIRouter()


class RegisterUserRequest(BaseModel):
    name: str
    email: str
    password: str


class RegisterUserResponse(BaseModel):
    id: str
    email: str


@router.post("/users/register", response_model=RegisterUserResponse)
def register_user(request: RegisterUserRequest):
    use_case = RegisterUser()
    try:
        result = use_case.__call__(
            name=request.name,
            email=request.email,
            password=request.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RegisterUserResponse(id=result.id, email=result.email)
```

**Usage in API Router:**
```python
from fastapi import FastAPI
from interfaces.controllers.user_controller import router as user_router

app = FastAPI()
app.include_router(user_router, prefix="/api")
```

## Notes
The `controllers` directory ensures a clear boundary between the interface layer and the application layer. By keeping controllers focused and delegating responsibilities appropriately, the application becomes more maintainable, testable, and scalable.

