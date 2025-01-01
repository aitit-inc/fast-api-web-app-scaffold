# DTO Directory

The `dto` (Data Transfer Object) directory contains classes and structures used for transferring data between layers of the application. DTOs are designed to encapsulate and validate the data required for input and output operations, ensuring a clear contract between components.

## Purpose
DTOs serve as a medium to:
- Validate and structure incoming data (e.g., from API requests or external sources).
- Transform domain data into a format suitable for external use (e.g., JSON responses).
- Decouple the domain layer from external representations of data.

## Structure
All DTOs are stored in a flat structure within the `dto` directory to maintain simplicity and ease of navigation. This approach works best for smaller projects or when the number of DTOs is manageable.

```
dto/
|-- register_user_dto.py  # Example DTO for user registration
|-- user_response_dto.py  # Example DTO for user response
|-- ...                   # Additional DTOs
```

## Principles
1. **Validation:** Ensure all DTOs validate their data before passing it to the next layer.
2. **Separation of Concerns:** Use DTOs to isolate input/output concerns from domain logic.
3. **Consistency:** Standardize data formats across all components to reduce potential errors.

## Guidelines
- Keep DTOs lightweight and focused on a specific purpose (input or output).
- Avoid embedding business logic in DTOs; they should only handle data transformation and validation.
- Use type hints and validation libraries (e.g., Pydantic, Marshmallow) to ensure data integrity.

## Example
**DTO: `RegisterUserDTO`**
```python
from pydantic import BaseModel, EmailStr

class RegisterUserDTO(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "securepassword123"
            }
        }
```

**DTO: `UserResponseDTO`**
```python
from pydantic import BaseModel

class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "id": "12345",
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
```

## Notes
By keeping the `dto` directory flat, it simplifies file management and avoids unnecessary nesting. This structure works well for projects with a moderate number of DTOs, ensuring clarity and ease of access while maintaining consistency in data handling.

