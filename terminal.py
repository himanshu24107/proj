import mysql.connector
from datetime import datetime

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS wholesale;')
mycursor.execute('USE wholesale;')
# Create the inventory table if it doesn't exist
mycursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    orderid INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(50),
    qty INT,
    rate DECIMAL(10,2),
    price DECIMAL(10,2),
    date DATE
)
""")

# Function to add incoming items
def add_incoming():
    item = input("Enter item name: ")
    qty = int(input("Enter quantity: "))
    rate = float(input("Enter rate: "))
    price = qty * rate
    date = datetime.now().strftime("%Y-%m-%d")
    sql = "INSERT INTO inventory (item, qty, rate, price, date) VALUES (%s, %s, %s, %s, %s)"
    val = (item, qty, rate, price, date)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Incoming item added successfully!")

# Function to remove outgoing items
def remove_outgoing():
    orderid = input("Enter orderid: ")
    qty = int(input("Enter quantity to remove: "))
    mycursor.execute("SELECT * FROM inventory WHERE orderid = %s", (orderid,))
    result = mycursor.fetchone()
    if result:
        current_qty = result[2]
        if qty > current_qty:
            print("Quantity exceeds available stock!")
            return
        new_qty = current_qty - qty
        if new_qty == 0:
            mycursor.execute("DELETE FROM inventory WHERE orderid = %s", (orderid,))
        else:
            mycursor.execute("UPDATE inventory SET qty = %s WHERE orderid = %s", (new_qty, orderid))
        mydb.commit()
        print("Outgoing item removed successfully!")
    else:
        print("Item not found in inventory!")

# Function to check inventory
def check_inventory():
    mycursor.execute("SELECT item, qty FROM inventory")
    result = mycursor.fetchall()

    if result:
        print("Inventory:")
        for row in result:
            print(f"- {row[0]}: {row[1]}")
    else:
        print("No items in inventory.")

# Main loop
while True:
    print("\nWholesale Billing System")
    print("1. Add incoming item")
    print("2. Remove outgoing item")
    print("3. Check inventory")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_incoming()
    elif choice == '2':
        remove_outgoing()
    elif choice == '3':
        check_inventory()
    elif choice == '4':
        break
    else:
        print("Invalid choice!")
