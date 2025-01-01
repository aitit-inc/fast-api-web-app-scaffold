# Views Directory

The `views` directory contains components responsible for rendering responses to users or external systems. Views typically transform data into formats such as HTML, JSON, or XML and define how the application presents information to its consumers.

## Purpose
The purpose of the `views` directory is to:
- Manage the presentation logic for rendering responses.
- Provide templates and rendering utilities for web-based outputs.
- Standardize response formats across different endpoints and interfaces.

## Structure
The directory is organized by features or modules to ensure clarity and maintainability:

```
interfaces/views/
|-- user_views.py        # Views for user-related endpoints
|-- order_views.py       # Views for order-related endpoints
|-- product_views.py     # Views for product-related endpoints
```

## Principles
1. **Presentation Focus:** Views should focus solely on presenting data, delegating business logic to the application or domain layers.
2. **Consistency:** Ensure consistent response formats across all views.
3. **Separation of Concerns:** Keep presentation logic separate from data transformation and business rules.

## Guidelines
- Use views to format and structure responses for users or external systems.
- Employ templates or rendering engines (e.g., Jinja2 for HTML) when needed.
- Standardize error messages and status codes to enhance user experience.
- Avoid embedding business logic in views; delegate it to the appropriate service or use case.

## Example
**View: `user_views.py`**
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class UserViews:
    @staticmethod
    def render_user_detail(user):
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(
            status_code=200,
            content={
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        )

    @staticmethod
    def render_user_list(users):
        return JSONResponse(
            status_code=200,
            content=[
                {"id": user.id, "name": user.name, "email": user.email} for user in users
            ]
        )
```

**Usage in Controller:**
```python
from interfaces.views.user_views import UserViews

@router.get("/users/{user_id}")
def get_user(user_id: str):
    user = user_service.get_user_by_id(user_id)
    return UserViews.render_user_detail(user)

@router.get("/users")
def list_users():
    users = user_service.list_all_users()
    return UserViews.render_user_list(users)
```

## Notes
The `views` directory ensures a clear separation between how data is presented and how it is processed. By centralizing rendering logic, the application becomes more maintainable, scalable, and user-friendly.

