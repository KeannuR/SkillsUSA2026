from collections import defaultdict


ADMIN_USER = "SkillsUSA2026"
ADMIN_PASS = "1478IsAwesome@2026"
TAX_RATE = 0.08




## INVENTORY SHOULD BE FORMATTED 
    #[
    #("Item1", Price, Quantity),
    #("Item2", 0.50, 100)
    #]

#Product -------------------------------------------------------------------
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sold = 0

    def __str__(self):
        return f"{self.name:<22} ${self.price:<8.2f} qty: {self.quantity}"

#Inventory ------------------------------------------------------------
class Inventory:
    def __init__(self, seed):
        self.items: dict[str, Product] = {}
        self.seed = seed
        for name, price, qty in seed:
            self.items[name] = Product(name, float(price), int(qty))

   

    def available(self) -> list[Product]:
        return [p for p in self.items.values() if p.quantity > 0]

    def all(self) -> list[Product]:
        return list(self.items.values())

    def get(self, name: str) -> Product | None:
        return self.items.get(name)

    def add(self, name: str, price: float, qty: int):
        if name in self.items:
            self.items[name].quantity += qty
            self.items[name].price = price
        else:
            self.items[name] = Product(name, price, qty)

    def remove(self, name: str) -> bool:
        if name in self.items:
            del self.items[name]
            return True
        return False

    def update(self, name: str, field: str, value) -> bool:
        product = self.items.get(name)
        if not product:
            return False
        if field == "price":
            product.price = float(value)
        elif field == "quantity":
            product.quantity = int(value)
        return True

# Handles shoppers cart
class Cart:
    def __init__(self):
        self.items: dict[str, int] = defaultdict(int)

    def add(self, product: Product, qty: int):
        self.items[product.name] += qty

    def remove(self, name: str):
        self.items.pop(name, None)

    def get_qty(self, name: str) -> int:
        return self.items.get(name, 0)

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def clear(self):
        self.items.clear()

    def subtotal(self, inventory: Inventory) -> float:
        total = 0.0
        for name, qty in self.items.items():
            product = inventory.get(name)
            if product:
                total += product.price * qty
        return total


#Store ─────────────────────────────────────────────────────────────────────

class Store:
    def __init__(self, seed):
        self.inventory = Inventory(seed)
        self.cart = Cart()
        self.gross_sales = 0.0

    #Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _header(title: str):
        print("\n" + "─" * 50)
        print(f"  {title}")
        print("─" * 50)

    @staticmethod
    def _input(prompt: str) -> str:
        return input(f"  {prompt}").strip()

    #Shop ──────────────────────────────────────────────────────────────────

    def shop(self):
        while True:
            self._header("SHOP — Available Items")
            items = self.inventory.available()
            if not items:
                print("  No items currently in stock.")
                return

            for i, product in enumerate(items, 1):
                in_cart = self.cart.get_qty(product.name)
                available = product.quantity - in_cart
                print(f"  [{i}] {product.name:<22} ${product.price:.2f}   "
                      f"(available: {available})")

            print("\n  [0] Back to Main Menu")
            choice = self._input("Select item #: ")

            if choice == "0":
                return

            if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
                print("  Invalid selection. Try again.")
                continue

            selected = items[int(choice) - 1]
            in_cart = self.cart.get_qty(selected.name)
            max_add = selected.quantity - in_cart

            qty_input = self._input(f"Quantity for {selected.name} (max {max_add}): ")

            if not qty_input.isdigit() or int(qty_input) <= 0:
                print("  Quantity must be a positive number.")
                continue

            qty = int(qty_input)
            if qty > max_add:
                print(f"  Cannot add {qty}. Only {max_add} available.")
                continue

            self.cart.add(selected, qty)
            print(f"  Added {qty}x {selected.name} to cart.")

    #Checkout ──────────────────────────────────────────────────────────────

    def checkout(self):
        if self.cart.is_empty():
            print("\n  Your cart is empty.")
            return

        self._header("CHECKOUT")
        print(f"  {'Item':<22} {'Qty':<6} {'Price':<10} Cost")
        print("  " + "-" * 44)

        subtotal = 0.0
        for name, qty in self.cart.items.items():
            product = self.inventory.get(name)
            if not product:
                continue
            cost = product.price * qty
            subtotal += cost
            print(f"  {name:<22} {qty:<6} ${product.price:<9.2f} ${cost:.2f}")

        tax = subtotal * TAX_RATE
        total = subtotal + tax

        print("  " + "-" * 44)
        print(f"  {'Subtotal:':<30} ${subtotal:.2f}")
        print(f"  {'Tax (8%):':<30} ${tax:.2f}")
        print(f"  {'TOTAL:':<30} ${total:.2f}")

        confirm = self._input("\nConfirm purchase? (y/n): ").lower()
        if confirm != "y":
            print("  Checkout cancelled.")
            return

        self._print_receipt(subtotal, tax, total)

        for name, qty in self.cart.items.items():
            product = self.inventory.get(name)
            if product:
                product.quantity -= qty
                product.sold += qty

        self.gross_sales += total
        self.cart.clear()

    def _print_receipt(self, subtotal: float, tax: float, total: float):
        from datetime import datetime
        self._header("RECEIPT")
        print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        for name, qty in self.cart.items.items():
            product = self.inventory.get(name)
            if product:
                print(f"  {name:<22} x{qty}   ${product.price * qty:.2f}")
        print()
        print(f"  {'Subtotal:':<28} ${subtotal:.2f}")
        print(f"  {'Tax (8%):':<28} ${tax:.2f}")
        print(f"  {'Total:':<28} ${total:.2f}")
        print("─" * 50)
        print("  Thank you for your purchase!")

    #Manager ───────────────────────────────────────────────────────────────

    def manager(self):
        self._header("MANAGER LOGIN")
        username = self._input("Username: ")
        password = self._input("Password: ")

        if username != ADMIN_USER or password != ADMIN_PASS:
            print("  Access denied. Invalid credentials.")
            return

        print("  Access granted.")
        self._manager_menu()

    def _manager_menu(self):
        while True:
            self._header("MANAGER PANEL")
            print("  [1] View Sales Report")
            print("  [2] Add Item")
            print("  [3] Remove Item")
            print("  [4] Update Item")
            print("  [5] Back to Main Menu")

            choice = self._input("Select option: ")

            if choice == "1":
                self._sales_report()
            elif choice == "2":
                self._add_item()
            elif choice == "3":
                self._remove_item()
            elif choice == "4":
                self._update_item()
            elif choice == "5":
                return
            else:
                print("  Invalid option.")

    def _sales_report(self):
        self._header("SALES REPORT")
        sold_any = False
        for product in self.inventory.all():
            if product.sold > 0:
                print(f"  {product.name:<22} sold: {product.sold}")
                sold_any = True
        if not sold_any:
            print("  No sales recorded yet.")
        print(f"\n  Gross Sales: ${self.gross_sales:.2f}")

    def _add_item(self):
        self._header("Add New Item")
        name = self._input("Item name (0 to cancel): ")
        if name == "0":
            return

        price_input = self._input("Price: $")
        try:
            price = float(price_input)
            if price <= 0:
                raise ValueError
        except ValueError:
            print("  Invalid price.")
            return

        qty_input = self._input("Quantity: ")
        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("  Invalid quantity.")
            return

        self.inventory.add(name, price, int(qty_input))
        print(f"  Added \"{name}\" (${price:.2f} x{qty_input}).")

    def _remove_item(self):
        self._header("Remove Item")
        all_items = self.inventory.all()
        for i, p in enumerate(all_items, 1):
            print(f"  [{i}] {p.name}")
        choice = self._input("Enter item # to remove (0 to cancel): ")
        if choice == "0":
            return
        if not choice.isdigit() or not (1 <= int(choice) <= len(all_items)):
            print("  Invalid.")
            return
        name = all_items[int(choice) - 1].name
        self.inventory.remove(name)
        print(f"  Removed \"{name}\".")

    def _update_item(self):
        self._header("Update Item")
        all_items = self.inventory.all()
        for i, p in enumerate(all_items, 1):
            print(f"  [{i}] {p.name:<22} ${p.price:.2f}   qty: {p.quantity}")
        choice = self._input("Enter item # to update (0 to cancel): ")
        if choice == "0":
            return
        if not choice.isdigit() or not (1 <= int(choice) <= len(all_items)):
            print("  Invalid selection.")
            return

        product = all_items[int(choice) - 1]
        print(f"\n  Updating: {product.name}")
        print("  [1] Price")
        print("  [2] Quantity")
        field_choice = self._input("Update which field? ")

        if field_choice == "1":
            val = self._input("New price: $")
            try:
                price = float(val)
                if price < 0:
                    raise ValueError
            except ValueError:
                print("  Invalid price.")
                return
            self.inventory.update(product.name, "price", price)
            print(f"  Price updated to ${price:.2f}.")

        elif field_choice == "2":
            val = self._input("New quantity: ")
            if not val.isdigit() or int(val) < 0:
                print("  Invalid quantity.")
                return
            self.inventory.update(product.name, "quantity", int(val))
            print(f"  Quantity updated to {val}.")
        else:
            print("  Invalid field choice.")

    #Main Loop ─────────────────────────────────────────────────────────────

    def run(self):
        print("\n" + "=" * 50)
        print("       WELCOME TO STOREMS")
        print("=" * 50)

        while True:
            self._header("MAIN MENU")
            cart_count = sum(self.cart.items.values())
            if cart_count > 0:
                sub = self.cart.subtotal(self.inventory)
                print(f"  Cart: {cart_count} item(s) | ${sub:.2f}\n")
            print("  [1] Shop")
            print("  [2] Checkout")
            print("  [3] Manager")
            print("  [4] Exit")

            choice = self._input("Select option: ")

            if choice == "1":
                self.shop()
            elif choice == "2":
                self.checkout()
            elif choice == "3":
                self.manager()
            elif choice == "4":
                print("\n  Goodbye!\n")
                break
            else:
                print("  Invalid option. Please choose 1–4.")

def init():
    startingInventory =  [
            ("Apple",          0.99, 50),
            ("SkillsUSA Suits", 100, 2), #only 2 because it was impossible to get any.
            ("SkillsUSA Polos", 20, 3 ), #couldn't get one either.
            ("Banana", 0.50, 100),
            ("Cereal", 2, 40)
        ]
    store = Store(startingInventory)
    store.run()
# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init()
