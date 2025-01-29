import tkinter as tkk
from tkinter import simpledialog, messagebox, ttk

# Inventory with categories, each item stored in dictionary with category as key
inventory = {
    "Snacks": {
        "A1": ["Lays Stax Original", 7.95, 10], # Item format: Name, Price, Stock
        "A2": ["Doritos Nacho Cheese ", 2.25, 10],
        "A3": ["Pringles", 14.50, 15],
        "A4": ["Ruffles Original Potato Chips", 5.70, 10],
        "A5": ["Takis", 8.50, 10],
        "A6": ["KitKat", 4.75, 10],
        "A7": ["Cadbury Dairy Milk", 9.00, 10],
        "A8": ["Chips Original Chocolate Cookies", 5.50, 20],
    },
    "Beverages": {
        "B1": ["Coke Zero", 2.50, 15],
        "B2": ["Sprite", 2.50, 15],
        "B3": ["Schweppes", 3.00, 10],
        "B4": ["Pepsi", 2.50, 15],
        "B5": ["7UP", 2.50, 15],
        "B6": ["Fanta", 2.50, 10],
        "B7": ["Masafi Natural Mineral Water", 1.25, 10],
        "B8": ["Al Ain Water", 1.00, 10],
        "B9": ["Red Bull", 7.00, 10],
        "B10": ["Monster Energy", 9, 10],
        "B11": ["Tropicana", 10.00, 10],
        "B12": ["Del Monte", 2.50, 15],
    },
    "Frozen Items": {
        "C1": ["Magnum Ice Cream Bar", 7.00, 8],
        "C2": ["Pizza Hut Frozen Pizza", 15.00, 8],
        "C3": ["Cornetto Ice Cream Cone", 6.00, 10],
        "C4": ["Ben & Jerry’s Ice Cream Cup", 15, 6],
        "C5": ["Al Marai Samosas", 10.00, 10],
        "C6": ["Frozen Burrito", 7.50, 8],
        "C7": ["Eggo Frozen Waffles", 15.00, 10],
        "C8": ["Pancakes", 10.00, 6],
    },
    "Healthy Options": {
        "D1": ["Quest Protein Bar", 15.00, 10],
        "D2": ["Clif Bar", 8.50, 12],
        "D3": ["Mixed Nuts", 12.00, 8],
        "D4": ["Craisins Dried Cranberries", 10.00, 15],
        "D5": ["SlimFast Protein Shake", 15.00, 10],
        "D6": ["Rice Cakes", 6.00, 12],
        "D7": ["Fresh Mixed Fruit Cup", 10.00, 8],
        "D8": ["Baked Veggie Chips", 7.00, 15],
        "D9": ["Vita Coco Coconut Water’s", 9.00, 15],
        "D10": ["Zico Coconut Water", 10.00, 8],
        "D11": ["Vegan Protein Bar", 18.00, 10],
        "D12": ["Vegan Jerky", 15.00, 12],
    },
}

cart = []   # Cart to store selected items
PASSWORD = "AEadmin0923" # Admin password for admin panel

def update_inventory(): # Update inventory display within the grid
    for widget in FrameInventory.winfo_children():
        widget.destroy()    #Clear current display
    row = 0
    for category, items in inventory.items():
        tkk.Label(FrameInventory, text=category, font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=4, sticky="w", pady=(10, 5))
        row += 1
        col = 0
        for code, (name, price, stock) in items.items():
            # Create frame for each item
            FrameItem = tkk.Frame(FrameInventory, bd=1, relief="solid", padx=10, pady=10, width=100, height=100)
            FrameItem.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            FrameItem.grid_propagate(False)

            # Display item details
            tkk.Label(FrameItem, text=f"Code: {code}").pack()
            tkk.Label(FrameItem, text=f"Name: {name}").pack()
            tkk.Label(FrameItem, text=f"Price: ${price:.2f}").pack()
            tkk.Label(FrameItem, text=f"Stock: {stock}").pack()

            col += 1
            if col >= 4:    # 4 items per row
                col = 0
                row += 1

def select_item(ItemCode):   # Add selected item to the cart and reduce stock
    global cart
    for category, items in inventory.items():
        if ItemCode in items:
            NameItem, PriceItem, StockItem = items[ItemCode]
            if StockItem > 0:
                # Add to cart and reduce stock
                cart.append((category, ItemCode, NameItem, PriceItem))
                inventory[category][ItemCode][2] = max(0, inventory[category][ItemCode][2] - 1)  # Ensure stock doesn't go below 0
                update_inventory()  # Update inventory display
                update_cart()  # Update the cart display
            else:
                messagebox.showerror("Stock error", f"You can not select more of any of {NameItem}.")
            return
    messagebox.showerror("Invalid Item", "The selected item code is not valid.")

def insert_money(): # Allow to insert money temporarily for the purchase of items
    try:
        amount = float(simpledialog.askstring("Insert Money", "Enter amount to insert:"))
        if amount > 0:
            money = amount
            MoneyLabel.config(text=f"Inserted Money: ${money:.2f}")
        else:
            messagebox.showerror("Error", "Please enter a positive amount.")
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Invalid input, Please enter a numeric value.")

def update_cart():  # Update the cart display in the GUI
    ContentCart = "\n".join([f"{item[2]} - ${item[3]:.2f}" for item in cart])
    TotalPrice = sum([item[3] for item in cart])  # Calculate total price of items in cart
    if ContentCart:
        CartLabel.config(text=f"Items in your cart:\n{ContentCart}")
        TotalLabel.config(text=f"Total: ${TotalPrice:.2f}")  # Display total price within cart
    else:
        CartLabel.config(text="Your cart is empty.")
        TotalLabel.config(text="Total: $0.00")  # Reset if the cart is empty

def purchase_item(): # Completes the purchase and updates the inventory
    global cart
    if cart:
        TotalPrice = sum([item[3] for item in cart])  # Calculate total price of items in the cart
        money = float(MoneyLabel.cget("text").split("$")[-1])  # Get the inserted money amount
        if money >= TotalPrice:
            for category, item_code, item_name, item_price in cart:
                # Subtract stock for each item in cart, making sure to not go below zero or negative values
                inventory[category][item_code][2] = max(0, inventory[category][item_code][2] - 1)
            update_inventory()
            change = money - TotalPrice  # Calculate leftover change
            MoneyLabel.config(text=f"Inserted Money: $0.00")  # Reset money after purchase
            ResultLabel.config(text=f"Purchased Items:\n{'\n'.join([item[2] for item in cart])}\nChange: ${change:.2f}")
            cart = []  # Clear cart after purchase
            update_cart()  # Reset cart display in GUI
        else:
            ResultLabel.config(text=f"Lack of funds. Total: ${TotalPrice:.2f}")
    else:
        ResultLabel.config(text="No items in the cart")

def admin_panel():  # Open admin panel for managing inventory
    # Simple admin login check
    password = simpledialog.askstring("Admin Login", "Enter password:")
    if password == PASSWORD:
        # If password matches, show admin options
        admin_window = tkk.Toplevel(root)

        # Ask for the item code to update
        item_code = simpledialog.askstring("Item Code", "Enter the item code to update:", parent=admin_window)

        if item_code:
            item_code = item_code.upper()  # Convert item_code to uppercase to match inventory codes

            # Check if the item code exists
            item_found = False
            for category, items in inventory.items():
                if item_code in items:
                    item_found = True
                    # Retrieve current price and stock
                    current_price = items[item_code][1]
                    current_stock = items[item_code][2]

                    # Ask for the new price and stock, show current values
                    new_price = simpledialog.askfloat("New Price", f"Current Price: ${current_price}\nEnter new price for {items[item_code][0]}:", parent=admin_window)
                    new_stock = simpledialog.askinteger("New Stock", f"Current Stock: {current_stock}\nEnter new stock for {items[item_code][0]}:", parent=admin_window)

                    # Update the item's price and stock
                    inventory[category][item_code][1] = new_price  # Update price
                    inventory[category][item_code][2] = new_stock  # Update stock

                    messagebox.showinfo("Update Successful", f"Updated {items[item_code][0]} - Price: ${new_price}, Stock: {new_stock}")
                    update_inventory()  # Update the inventory display
                    break
            if not item_found:
                messagebox.showerror("Item Not Found", "The item code you entered is not valid.")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid item code.")
    else:
        messagebox.showerror("Access Denied", "Password Incorrect")
    
def update_item_dropdown(*args):
    # Update the ItemCodeCombo dropdown based on the selected category  
    selected_category = CategoryCombo.get()
    if selected_category in inventory:
        item_codes = list(inventory[selected_category].keys())
        ItemCodeCombo['values'] = item_codes
        ItemCodeCombo.set("")  # Reset the item code selection

# Create Window
root = tkk.Tk()
root.title("Vending Machine")

root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Set the window to fullscreen

# Inventory display
InventoryLabel = tkk.Label(root, text="Available Items:")
InventoryLabel.pack()

# Create a frame for the inventory with a canvas
Layout = tkk.Canvas(root)
Layout.pack(side="left", fill="both", expand=True)

# Make vertical scrollbar
ScrollBar = tkk.Scrollbar(root, orient="vertical", command=Layout.yview) 
ScrollBar.pack(side="right", fill="y")

# Scrollbar for scrolling between different items
Layout.config(yscrollcommand=ScrollBar.set) 

# Create frame inside canvas
FrameInventory = tkk.Frame(Layout)
Layout.create_window((0, 0), window=FrameInventory, anchor="nw")

# Making sure scroll region updates dynamically as items are added
FrameInventory.bind("<Configure>",lambda e: Layout.configure(scrollregion=Layout.bbox("all")))

# Populate the inventory display initially
update_inventory()  

# Dropdown menu for selecting category
tkk.Label(root, text="Select Category:").pack()
CategoryCombo = ttk.Combobox(root, values=list(inventory.keys()))
CategoryCombo.pack()

CategoryCombo.bind("<<ComboboxSelected>>", update_item_dropdown)

# Item Code dropdown for item selection
tkk.Label(root, text="Select Item Code:").pack()
ItemCodeCombo = ttk.Combobox(root)
ItemCodeCombo.pack()

# Select button to add item to cart
SelectButton = tkk.Button(root, text="Select Item", command=lambda: select_item(ItemCodeCombo.get()))
SelectButton.pack()

# Insert money button to add money to the purchase
InsertMoneyButton = tkk.Button(root, text="Insert Money", command=insert_money)
InsertMoneyButton.pack()

# Label to display inserted money
MoneyLabel = tkk.Label(root, text="Inserted Money: $0.00")
MoneyLabel.pack()

# Cart display label
CartLabel = tkk.Label(root, text="Your cart is empty.")
CartLabel.pack()

# Total display label
TotalLabel = tkk.Label(root, text="Total: $0.00")
TotalLabel.pack()

# Purchase button
PurchaseButton = tkk.Button(root, text="Purchase", command=purchase_item)
PurchaseButton.pack()

# Label to display result
ResultLabel = tkk.Label(root, text="")
ResultLabel.pack()

# Admin button
AdminButton = tkk.Button(root, text="Admin Configuration", command=admin_panel, bg="red", fg="white")
AdminButton.pack()

# Run Tkinter event loop to keep application running
root.mainloop()