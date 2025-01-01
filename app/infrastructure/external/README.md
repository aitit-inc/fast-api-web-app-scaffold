# External Directory

The `external` directory contains integrations with external systems, APIs, and services. This directory acts as the gateway for communicating with third-party services, ensuring that interactions are encapsulated and do not leak into other layers of the application.

## Purpose
The purpose of the `external` directory is to:
- Provide a centralized location for managing third-party integrations.
- Abstract external APIs or services to maintain loose coupling with the application.
- Handle error cases, retries, and other robustness mechanisms for external communication.

## Structure
The directory is organized to separate different external services for better maintainability:

```
infrastructure/external/
|-- api_client.py        # General API client utilities
|-- payment_gateway.py   # Integration with a payment gateway
|-- email_service.py     # Integration with an email delivery service
|-- sms_provider.py      # Integration with an SMS provider
```

## Principles
1. **Encapsulation:** Encapsulate external service logic to prevent it from spreading across the application.
2. **Resilience:** Implement retry mechanisms, error handling, and logging for external communication.
3. **Configuration:** Use environment variables or configuration files to manage credentials and settings for external services.

## Guidelines
- Use specific modules or classes for each external service to keep the codebase organized.
- Leverage libraries or SDKs provided by third-party services where appropriate.
- Log errors and unexpected behaviors during external interactions to assist debugging.
- Securely store and access API keys, credentials, and sensitive data through configuration files or secret management tools.

## Example
**API Client Utility: `api_client.py`**
```python
import requests

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()
```

**Integration Example: `payment_gateway.py`**
```python
from infrastructure.external.api_client import APIClient

class PaymentGateway:
    def __init__(self, base_url, api_key):
        self.client = APIClient(base_url, api_key)

    def process_payment(self, amount, currency, source):
        data = {
            "amount": amount,
            "currency": currency,
            "source": source
        }
        return self.client.post("payments", data)
```

**Usage in Application Layer:**
```python
from infrastructure.external.payment_gateway import PaymentGateway

gateway = PaymentGateway(base_url="https://api.paymentprovider.com", api_key="your_api_key")
result = gateway.process_payment(100.0, "USD", "credit_card_source")
print(result)
```

## Notes
The `external` directory centralizes all third-party integrations, promoting modularity and ease of maintenance. By encapsulating these interactions, the application remains loosely coupled to external services, making it more resilient to changes and easier to test.

