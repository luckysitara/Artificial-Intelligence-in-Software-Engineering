class InvalidProductDataError(Exception):
    """Exception raised for invalid product data assignments."""
    pass


class Product:
    def __init__(self, name: str, price: float, quantity: float):
        self.name = name
        # Setters will be called, validating values at initialization
        self.price = price
        self.quantity = quantity

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise InvalidProductDataError(
                f"Invalid type for name: expected str, got {type(value).__name__}."
            )
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidProductDataError(
                f"Invalid type for price: expected a number, got {type(value).__name__}."
            )
        if value < 0:
            raise InvalidProductDataError(
                f"Invalid value for price: must be a non-negative number, got {value}."
            )
        self._price = float(value)

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidProductDataError(
                f"Invalid type for quantity: expected a number, got {type(value).__name__}."
            )
        if value < 0:
            raise InvalidProductDataError(
                f"Invalid value for quantity: must be a non-negative number, got {value}."
            )
        self._quantity = value


class InventoryManager:
    """Manages the collection of products and provides inventory operations."""
    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product):
        self.inventory.append(product)

    def update_quantity(self, name, new_quantity):
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                break

    def calculate_total_value(self):
        total = 0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        for product in self.inventory:
            print(f"{product.name} - ${product.price:.2f} x {product.quantity}")


# Demo Usage
manager = InventoryManager()
manager.add_product(Product("Laptop", 1200.00, 5))
manager.add_product(Product("Mouse", 25.00, 20))
manager.update_quantity("Mouse", 18)

print("Current Inventory:")
manager.display_inventory()
print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}")

# --- Testing Invalid Input ---
print("\n--- Testing Invalid Input ---")
try:
    manager.inventory[0].quantity = -5
except Exception as e:
    print(f"Test result: {e}")

# --- Additional edge-case tests ---
print("\n--- Testing Invalid Type (bool as quantity) ---")
try:
    manager.inventory[0].quantity = True
except Exception as e:
    print(f"Test result: {e}")

print("\n--- Testing Invalid Type (string as price) ---")
try:
    manager.inventory[0].price = "expensive"
except Exception as e:
    print(f"Test result: {e}")

print("\n--- Testing Invalid Name Type ---")
try:
    manager.inventory[0].name = 12345
except Exception as e:
    print(f"Test result: {e}")
