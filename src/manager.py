import os
from costumer import view_all_drinks, place_order, pay_for_order, save_to_receipt, update_stock
import matplotlib.pyplot as plt
import datetime

def launch_manager_form():
    while(True):
        print("Welcome manager!")
        print("1. Order more items")
        print("2. Remove items")
        print("3. View all receipts")
        print("4. View profit")
        print("5. View all drinks and prices")
        print("6. Place an order")
        print("7. Change the price of an item")
        print("8. Pay for order")
        print("9. Trasfer money")
        print("10. Statistics")
        print("11. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            order_more_items()
        elif choice == "2":
            remove_items()
        elif choice == "3":
            view_all_receipts()
        elif choice == "4":
            view_profit()
        elif choice == "5":
            view_all_drinks()
        elif choice == "6":
            place_order()
        elif choice == "7":
            change_price()
        elif choice == "8":
            pay_for_order()
        elif choice == "9":
            transfer_money()
        elif choice == "10":
            create_statistics()
        elif choice == "11":
            break
        else:
            print("Invalid choice. Exiting...")


def order_more_items():
    item = input("Enter the name of the item you want to order more of: ")
    quantity = input("Enter the quantity you want to order: ")
    if not os.path.exists("res/files/pricesForItems.txt"):
        print("pricesForItems.txt does not exist.")
        return
    item_exists = False
    with open("res/files/pricesForItems.txt", "r") as f:
        for line in f:
            name, price = line.strip().split(":")
            if name == item:
                item_exists = True
                priceB = float(price)
                break
    if not item_exists:
        print(f"{item} is not listed in pricesForItems.txt.")
        return
    if not os.path.exists("res/money/forOrders.txt"):
        print("forOrders.txt does not exist.")
        return
    with open("res/money/forOrders.txt", "r") as f:
        money = float(f.read())
    if money < priceB * int(quantity):
        print("Not enough money in forOrders.txt.")
        return
    if not os.path.exists("res/files/items.txt"):
        print("items.txt does not exist.")
        return
    with open("res/files/items.txt", "r") as f:
        lines = f.readlines()
    created = False
    with open("res/files/items.txt", "w") as f:
        for line in lines:
            name, price, stock = line.strip().split(":")
            if name == item:
                stock = str(int(stock) + int(quantity))
                update_money_for_orders(-priceB * int(quantity))
                print(f"{quantity} units of {item} have been ordered.")
                f.write(f"{name}:{price}:{stock}\n")
                created = True
            else:
                f.write(line)
        if not created:
            f.write(f"{item}:{price}:{quantity}\n")
            update_money_for_orders(-priceB * int(quantity))
            print(f"{quantity} units of {item} have been ordered.")


def update_money_for_orders(amount):
    if not os.path.exists("res/money/forOrders.txt"):
        with open("res/money/forOrders.txt", "w") as f:
            f.write("0")
    with open("res/money/forOrders.txt", "r") as f:
        money = float(f.read())
    money += amount
    with open("res/money/forOrders.txt", "w") as f:
        f.write(str(money))


def change_price():
    item = input("Enter the name of the item whose price you want to change: ")
    new_price = input("Enter the new price: ")
    if not os.path.exists("res/files/items.txt"):
        print("items.txt does not exist.")
        return
    with open("res/files/items.txt", "r") as f:
        lines = f.readlines()
    with open("res/files/items.txt", "w") as f:
        item_exists = False
        for line in lines:
            name, price, stock = line.strip().split(":")
            if name == item:
                item_exists = True
                f.write(f"{name}:{new_price}:{stock}\n")
            else:
                f.write(line)
        if not item_exists:
            print(f"{item} does not exist in items.txt.")
    if item_exists:
        print(f"Price of {item} changed to ${new_price}")


def transfer_money():
    # if profit does not exist, create it
    if not os.path.exists("res/money/profit.txt"):
        with open("res/money/profit.txt", "w") as f:
            f.write("0")
    with open("res/money/profit.txt", "r") as f:
        profit = float(f.read())
    transfer_amount = float(input("Enter the amount you want to transfer: "))
    if transfer_amount > profit:
        print("Insufficient funds.")
        return
    profit -= transfer_amount
    with open("res/money/profit.txt", "w") as f:
        f.write(str(profit))
    if not os.path.exists("res/money/forOrders.txt"):
        with open("res/money/forOrders.txt", "w") as f:
            f.write("0")
    with open("res/money/forOrders.txt", "r") as f:
        money = float(f.read())
    money += transfer_amount
    with open("res/money/forOrders.txt", "w") as f:
        f.write(str(money))
    print(f"{transfer_amount} transferred from profit to forOrders.txt.")


def view_all_receipts():
    receipts_path = "res/receipts"
    if not os.path.exists(receipts_path):
        print("No receipts found.")
        return
    for filename in os.listdir(receipts_path):
        if filename.startswith("receipt"):
            paid = False
            summary = 0
            with open(os.path.join(receipts_path, filename)) as f:
                lines = f.readlines()
                print(f"Receipt {filename}:")
                if lines.__contains__("checked"):
                    print("This receipt has already been checked.")
                    continue
                for line in lines:
                    if line.strip() == "Paid":
                        paid = True
                        break
                    name, price = line.strip().split(":")
                    priceOfItem = float(price)
                    print(f"{name} - ${price}")
                if paid:
                    print(f"Receipt {filename} is paid.")
                    for line in lines:
                        if line.strip() == "Paid":
                            break
                        name, price = line.strip().split(":")
                        summary += calculate_profit(name, float(price))
                    update_profit(summary)
                else:
                    print(f"Receipt {filename} is not paid.")
            with open(os.path.join(receipts_path, filename), 'a') as f:
                f.write("checked")



def calculate_profit(name, priceOfItem):
    with open("res/files/items.txt", "r") as f:
        for line in f:
            item_name, item_price, stock = line.strip().split(":")
            if item_name == name:
                priceOfItemStock = float(item_price)
                break
    with open("res/files/pricesForItems.txt", "r") as f:
        for line in f:
            item_name, item_price = line.strip().split(":")
            if item_name == name:
                priceOfItemStock = float(item_price)
                break
    return priceOfItem - priceOfItemStock


def update_profit(amount):
    if not os.path.exists("res/money/profit.txt"):
        with open("res/money/profit.txt", "w") as f:
            f.write("0")
    with open("res/money/profit.txt", "r") as f:
        profit = float(f.read())
    profit += amount
    with open("res/money/profit.txt", "w") as f:
        f.write(str(profit))



def remove_items():
    item = input("Enter the name of the item you want to remove: ")
    with open("res/files/items.txt", "r") as f:
        lines = f.readlines()
    with open("res/files/items.txt", "w") as f:
        for line in lines:
            name, price, stock = line.strip().split(":")
            if name != item:
                f.write(line)
    print(f"{item} has been removed.")



def view_profit():
    money_path = "res/money"
    if not os.path.exists(money_path):
        print("No money found.")
        return
    profit = 0
    for filename in os.listdir(money_path):
        if filename.startswith("day"):
            with open(os.path.join(money_path, filename)) as f:
                for line in f:
                    profit += float(line)
    print(f"Profit for this month is ${profit}")


def create_statistics():
    now = datetime.datetime.now()
    day = now.strftime("%d")
    statistics_path = "res/files/statistics" + day + ".txt"
    if not os.path.exists(statistics_path):
        with open(statistics_path, "w") as f:
            pass
    item_count = {}
    for filename in os.listdir("res/receipts"):
        if filename.startswith("receipt"):
            with open(os.path.join("res/receipts", filename)) as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() == "Paid":
                        break
                    if line.strip() == "checked":
                        break
                    name, price = line.strip().split(":")
                    if name in item_count:
                        item_count[name] += 1
                    else:
                        item_count[name] = 1
    with open(statistics_path, "w") as f:
        for item, count in item_count.items():
            f.write(f"{item}:{count}\n")

    items = list(item_count.keys())
    counts = list(item_count.values())

    plt.plot(items, counts)
    plt.xlabel('Item')
    plt.ylabel('Count')
    plt.title('Statistics')
    plt.show()
