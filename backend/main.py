import redis

class InventoryManager:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def add_product(self, product_id, name, quantity):
        if self.r.exists(f"product:{product_id}"):
            raise ValueError("Product already exists.")
        self.r.hmset(f"product:{product_id}", {"name": name, "quantity": quantity})
        print("Product added successfully.")

    def update_product_quantity(self, product_id, quantity):
        if not self.r.exists(f"product:{product_id}"):
            raise ValueError("Product does not exist.")
        self.r.hset(f"product:{product_id}", "quantity", quantity)
        print("Product quantity updated successfully.")

    def remove_product(self, product_id):
        if not self.r.exists(f"product:{product_id}"):
            raise ValueError("Product does not exist.")
        self.r.delete(f"product:{product_id}")
        print("Product removed successfully.")

    def view_inventory(self):
        inventory = {}
        for key in self.r.scan_iter("product:*"):
            product_id = key.decode().split(":")[-1]
            product_details = self.r.hgetall(key)
            inventory[product_id] = {
                "name": product_details[b'name'].decode(),
                "quantity": int(product_details[b'quantity'].decode())
            }
        return inventory

def main():
    print("Initializing Inventory Management System...")
    inventory_manager = InventoryManager()
    print("Inventory Management System initialized successfully.")
    
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Update Product Quantity")
        print("3. Remove Product")
        print("4. View Inventory")
        print("5. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                product_id = input("Enter Product ID: ")
                name = input("Enter Product Name: ")
                quantity = int(input("Enter Quantity: "))
                inventory_manager.add_product(product_id, name, quantity)
            elif choice == '2':
                product_id = input("Enter Product ID: ")
                quantity = int(input("Enter New Quantity: "))
                inventory_manager.update_product_quantity(product_id, quantity)
            elif choice == '3':
                product_id = input("Enter Product ID: ")
                inventory_manager.remove_product(product_id)
            elif choice == '4':
                inventory = inventory_manager.view_inventory()
                print("\nInventory:")
                for product_id, details in inventory.items():
                    print(f"Product ID: {product_id}, Name: {details['name']}, Quantity: {details['quantity']}")
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
