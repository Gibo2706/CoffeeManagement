import random
import os
from datetime import date
receiptNumber = random.randint(100000, 999999)
def on_continue():
    while(True):
        print("Welcome guest!")
        print("1. View all drinks and prices")
        print("2. Place an order")
        print("3. Pay for order")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_drinks()
        elif choice == "2":
            place_order()
        elif choice == "3":
            pay_for_order()
            break
        else:
            print("Invalid choice. Exiting...")


def view_all_drinks():
    with open("res/files/items.txt", "r") as f:
        for line in f:
            item, price, stock = line.strip().split(":")
            print(f"{item}: {price} RSD (In stock: {stock})")


def place_order():
    item = input("Enter the name of the item you want to order: ")
    with open("res/files/items.txt", "r") as f:
        for line in f:
            name, price, stock = line.strip().split(":")
            if name == item:
                if stock == "0":
                    print(f"Sorry, {item} is out of stock.")
                else:
                    print(f"You have ordered {item} for {price} RSD.")
                    update_stock(item, -1)
                    save_to_receipt(name, price, receiptNumber)
                    return
    print(f"Sorry, {item} is not available.")


def save_to_receipt(name, price, receiptNumber):
    with open(f"res/receipts/receipt{receiptNumber}.txt", "a") as f:
        f.write(f"{name}:{price}\n")


def pay_for_order():
    if not os.path.exists(f"res/receipts/receipt{receiptNumber}.txt"):
        print("No order to pay for.")
        return

    total_price = 0    
    with open(f"res/receipts/receipt{receiptNumber}.txt", "r") as f:
        for line in f:
            name, price = line.strip().split(":")
            total_price += float(price)
            print(f"{name}: {price} RSD")
    while(True):
        print(f"Total price: {total_price} RSD")
        payment = input("Enter the amount paid: ")
        if float(payment) >= total_price:
            change = float(payment) - total_price
            print(f"Thank you for your payment. Your change is {change} RSD.")
            with open(f"res/receipts/receipt{receiptNumber}.txt", "a") as f:
                f.write("Paid\n")
            save_to_file(total_price)
            return
        else:
            print("Insufficient payment. Please try again.")


def save_to_file(total_price):
    if not os.path.exists("res/money"):
        os.makedirs("res/money")
    today = date.today()
    file_name = "day" + str(today.day) + ".txt"
    file_path = "res/money/" + file_name
    with open(file_path, "a") as f:
        f.write(str(total_price) + "\n")


def update_stock(item, amount):
    with open("res/files/items.txt", "r") as f:
        lines = f.readlines()
    with open("res/files/items.txt", "w") as f:
        for line in lines:
            name, price, stock = line.strip().split(":")
            if name == item:
                stock = str(int(stock) + amount)
            f.write(f"{name}:{price}:{stock}\n")
