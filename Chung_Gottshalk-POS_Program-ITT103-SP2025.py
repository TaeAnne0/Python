# Names: Twain Chung 20241016 Tae Anne Gottshalk 20247342
# Course: Programming Techniques
# Lecturer: Mr Jonathon Johnson
# Semester: Spring 2025

# Point of Sale System - T&T EXPRESS LTD

def main():
    global product_catalog
    product_catalog = initialize_product_catalog()

    while True:
        cart = {}  # Create an empty shopping cart
        print("\n--- T&T EXPRESS LTD ---")
        while True:
            display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                view_products()
            elif choice == '2':
                add_to_cart(cart)
            elif choice == '3':
                remove_from_cart(cart)
            elif choice == '4':
                view_cart(cart)
            elif choice == '5':
                if checkout(cart):  # Only break if checkout is successful
                    break
            elif choice == '6':
                print("Exiting POS System. Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

# Initialize the product catalog with items, prices, and stock levels
def initialize_product_catalog():
    return {
        "Lasco": {"price": 180.0, "stock": 100},
        "Tissue": {"price": 100.0, "stock": 120},
        "Orange": {"price": 120.0, "stock": 40},
        "Betty Milk": {"price": 350.0, "stock": 30},
        "Bread": {"price": 550.0, "stock": 40},
        "Eggs": {"price": 450.0, "stock": 50},
        "Tastees Cheese": {"price": 600.0, "stock": 35},
        "Chicken": {"price": 1200.0, "stock": 100},
        "Jasmine Rice": {"price": 300.0, "stock": 95},
        "Baked Beans": {"price": 180.0, "stock": 85},
        "Flour": {"price": 100.0, "stock": 90},
        "Sugar": {"price": 100.0, "stock": 45},
        "Salt": {"price": 80.0, "stock": 60},
        "Anchor Butter": {"price": 500.0, "stock": 80},
        "Ariel Detergent": {"price": 300.0, "stock": 95}
    }

# Display main menu options
def display_menu():
    print("\n1. View Products\n2. Add to Cart\n3. Remove from Cart\n4. View Cart\n5. Checkout\n6. Exit")

# Show available products with their prices and stock
def view_products():
    print("\n--- Product Catalog ---")
    for idx, (product, details) in enumerate(product_catalog.items(), 1):
        print(f"{idx}. {product} - JMD${details['price']} - Stock: {details['stock']}")

# Get product name by its number
def get_product_by_number(number):
    products = list(product_catalog.keys())
    if 1 <= number <= len(products):
        return products[number - 1]
    return None

# Add selected item to cart
def add_to_cart(cart):
    global product_catalog
    view_products()
    try:
        product_number = int(input("Enter item add to cart: "))
        product_name = get_product_by_number(product_number)
        if not product_name:
            print("This product does not exist.")
            return
        quantity = int(input("Enter quantity: "))
        if quantity <= product_catalog[product_name]['stock']:
            cart[product_name] = cart.get(product_name, 0) + quantity
            product_catalog[product_name]['stock'] -= quantity
            print(f"Added {quantity} {product_name}(s) to cart.")

            # Low stock warning
            if product_catalog[product_name]['stock'] <= 5:
                print(f" Warning: {product_name} stock is low! Only {product_catalog[product_name]['stock']} left.")

        else:
            print("We are currently out.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except KeyError:
        print("Product not found in catalog.")
        
# Remove selected item(s) from cart
def remove_from_cart(cart):
    if not cart:
        print("Cart is empty.")
        return

    print("\n--- Items in Cart ---")
    for idx, (product, quantity) in enumerate(cart.items(), 1):
        print(f"{idx}. {product} - Quantity: {quantity}")

    try:
        product_number = int(input("What would you like to remove?: "))
        products_in_cart = list(cart.keys())
        if not (1 <= product_number <= len(products_in_cart)):
            print("Invalid product number.")
            return

        product_name = products_in_cart[product_number - 1]
        quantity = int(input("Enter quantity to remove: "))

        if quantity >= cart[product_name]:
            product_catalog[product_name]['stock'] += cart[product_name]
            del cart[product_name]
            print(f"Removed {product_name} from cart.")
        else:
            cart[product_name] -= quantity
            product_catalog[product_name]['stock'] += quantity
            print(f"Removed {quantity} {product_name}(s) from cart.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# View cart contents and total cost
def view_cart(cart):
    if not cart:
        print("\nCart is empty.")
        return

    print("\n--- Your Cart ---")
    total = 0
    for product, quantity in cart.items():
        price = product_catalog[product]['price']
        subtotal = price * quantity
        total += subtotal
        print(f"{product}: {quantity} x JMD${price:.2f} = JMD${subtotal:.2f}")
    print(f"Total: JMD${total:.2f}")

# Handle checkout process
def checkout(cart):
    if not cart:
        print("Cart is empty. Cannot checkout.")
        return False

    subtotal = calculate_subtotal(cart)
    discount = apply_discount(subtotal)
    taxed_total = apply_tax(subtotal - discount)

    print_summary(subtotal, discount, taxed_total)

    # Allow customer to review and remove items
    while True:
        review_choice = input("\nWould you like to remove any item before checkout? (yes/no): ").strip().lower()
        if review_choice == 'yes':
            remove_from_cart(cart)
            subtotal = calculate_subtotal(cart)
            discount = apply_discount(subtotal)
            taxed_total = apply_tax(subtotal - discount)
            print_summary(subtotal, discount, taxed_total)
        elif review_choice == 'no':
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

    # Payment step
    while True:
        try:
            amount_received = float(input("Enter amount received (JMD$): "))
            if amount_received >= taxed_total:
                change = amount_received - taxed_total
                print_receipt(cart, subtotal, discount, taxed_total, amount_received, change)
                return True
            else:
                print("Insufficient amount. Please enter enough to cover the total.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Calculate subtotal
def calculate_subtotal(cart):
    return sum(product_catalog[product]['price'] * quantity for product, quantity in cart.items())

# Apply discount if eligible
def apply_discount(subtotal):
    if subtotal > 2500:
        discount = subtotal * 0.05
        print(f"\nDiscount applied: -JMD${discount:.2f}")
        return discount
    return 0

# Apply sales tax
def apply_tax(amount):
    tax = amount * 0.10
    return amount + tax

# Print checkout summary
def print_summary(subtotal, discount, total_due):
    print(f"\nSubtotal: JMD${subtotal:.2f}")
    if discount:
        print(f"Discount: -JMD${discount:.2f}")
    tax = (total_due - (subtotal - discount))
    print(f"Sales Tax (10%): JMD${tax:.2f}")
    print(f"Total Due: JMD${total_due:.2f}")

# Print final receipt
def print_receipt(cart, subtotal, discount, total_due, amount_received, change):
    print("\n--- Store Receipt ---")
    print("T&T EXPRESS LTD")
    print("-------------------------------")
    for product, quantity in cart.items():
        price = product_catalog[product]['price']
        total_price = price * quantity
        print(f"{product} - {quantity} x JMD${price:.2f} = JMD${total_price:.2f}")
    print("-------------------------------")
    print(f"Subtotal: JMD${subtotal:.2f}")
    if discount:
        print(f"Discount: -JMD${discount:.2f}")
    tax = (total_due - (subtotal - discount))
    print(f"Sales Tax: JMD${tax:.2f}")
    print(f"Total Due: JMD${total_due:.2f}")
    print(f"Amount Paid: JMD${amount_received:.2f}")
    print(f"Change: JMD${change:.2f}")
    print("\nThank you for supporting our small business! Come again!")

if __name__ == "__main__":
    main()
