# AI: Integrating Robust Error Handling in OOP

## Objective
Apply AI-driven scaffolding to enhance a refactored `Product` class by integrating robust exception handling and data validation using Python's `@property` decorators and a custom exception, improving the code's resilience and data integrity.

## Files in This Folder
- `original_code.py` — the starting Object-Oriented Product Inventory Manager, before validation was added.
- `refactored_code.py` — the AI-assisted refactored version, with `@property` setters on `name`, `price`, and `quantity`, plus a custom `InvalidProductDataError` exception.

## AI Prompt Used
```
Refactor the Product class below to add robust data validation using Python's @property decorators and setter methods for the 'price' and 'quantity' attributes. Both values must be validated as non-negative numbers on every assignment, including at initialization. Define a custom exception called InvalidProductDataError (subclassing Exception) and raise it with a clear, descriptive message whenever invalid data is assigned, instead of allowing the program to crash or silently store bad data. After providing the modified code, explain in detail how using @property setters combined with a custom exception enforces data integrity and encapsulation, specifically addressing why this approach is safer than direct attribute assignment.

[Product and InventoryManager classes were pasted here]
```

## What Changed
The AI (Gemini Code Assist) added:
- A custom `InvalidProductDataError(Exception)` class to signal validation failures with a clear, specific message.
- `@property` / `@<attr>.setter` pairs for `name`, `price`, and `quantity`, so every assignment (including inside `__init__`) is routed through validation logic instead of being stored directly.
- Type checks that explicitly exclude `bool`, since Python treats booleans as a subtype of `int`, which could otherwise let `True`/`False` silently pass a naive numeric check.
- Value checks that reject negative numbers for `price` and `quantity`.

## Test Case & Result
```python
print("\n--- Testing Invalid Input ---")
try:
    manager.inventory[0].quantity = -5
except Exception as e:
    print(f"Test result: {e}")
```

**Output:**
```
--- Testing Invalid Input ---
Test result: Invalid value for quantity: must be a non-negative number, got -5.
```

## Analysis
When `manager.inventory[0].quantity = -5` was executed, the `quantity` setter intercepted the assignment before it reached the object's internal state. It confirmed the value was a genuine number (excluding `bool`), confirmed it was non-negative, and raised `InvalidProductDataError` with a specific message rather than allowing `-5` to silently overwrite `_quantity`.

This is safer than direct attribute assignment because, without the setter, an invalid value would be stored without complaint, leaving the object in an inconsistent state that could corrupt downstream calculations (e.g., `calculate_total_value()` returning a distorted total). Routing every assignment through the setter enforces:
- **Encapsulation** — external code cannot bypass validation, since even the constructor's own assignments (`self.price = price`) go through the setter.
- **Data integrity** — the object guarantees its own internal state is always valid, rather than relying on every caller to validate inputs beforehand.

The custom exception adds further clarity: code calling into `Product` can catch `InvalidProductDataError` specifically, rather than guessing whether a generic `ValueError` or `TypeError` was the real cause of failure.
