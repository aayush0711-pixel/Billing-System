import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector as sql
from datetime import datetime

# --------------------------
# Database Connection Setup
# --------------------------
def connect_db():
    try:
        con = sql.connect(
            host="localhost",
            user="root",        
            password="Ayush07@",        
            database="billing_system"
        )
        return con
    except:
        messagebox.showerror("Database Error", "Database connection failed!")
        return None

# --------------------------
# Functions
# --------------------------
def add_item():
    name = item_name.get()
    qty = quantity.get()
    price = item_price.get()

    if name == "" or qty == "" or price == "":
        messagebox.showwarning("Input Error", "Please fill all item fields")
        return

    total = float(qty) * float(price)
    bill_tree.insert("", tk.END, values=(name, qty, price, total))
    update_total()

    item_name.set("")
    quantity.set("")
    item_price.set("")

def update_total():
    total = 0
    for child in bill_tree.get_children():
        total += float(bill_tree.item(child, "values")[3])
    total_amount.set(f"{total:.2f}")

def generate_bill():
    cname = customer_name.get()
    if cname == "":
        messagebox.showwarning("Missing Info", "Enter customer name!")
        return

    items = []
    for child in bill_tree.get_children():
        item_values = bill_tree.item(child, "values")
        items.append(f"{item_values[0]} (x{item_values[1]}) - ₹{item_values[3]}")
    item_str = "\n".join(items)

    total = float(total_amount.get())
    dt = datetime.now()

    con = connect_db()
    if con:
        cur = con.cursor()
        cur.execute("INSERT INTO bills (customer_name, date_time, items, total_amount) VALUES (%s, %s, %s, %s)",
                    (cname, dt, item_str, total))
        con.commit()
        con.close()
        messagebox.showinfo("Bill Saved", f"Bill saved successfully for {cname}")
        clear_all()

def clear_all():
    customer_name.set("")
    item_name.set("")
    quantity.set("")
    item_price.set("")
    total_amount.set("0.00")
    for child in bill_tree.get_children():
        bill_tree.delete(child)

def show_bills():
    con = connect_db()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bills ORDER BY bill_id DESC")
        records = cur.fetchall()
        con.close()

        top = tk.Toplevel(root)
        top.title("Saved Bills")
        top.geometry("650x400")
        top.config(bg="#FAFAFA")

        tk.Label(top, text="Saved Bills", font=("Arial", 16, "bold"), bg="#FAFAFA", fg="#333").pack(pady=10)

        tree = ttk.Treeview(top, columns=("ID", "Customer", "Date", "Total"), show="headings")
        tree.heading("ID", text="Bill ID")
        tree.heading("Customer", text="Customer Name")
        tree.heading("Date", text="Date & Time")
        tree.heading("Total", text="Total Amount")

        tree.column("ID", width=60, anchor="center")
        tree.column("Customer", width=150)
        tree.column("Date", width=200)
        tree.column("Total", width=100, anchor="center")

        for r in records:
            tree.insert("", tk.END, values=(r[0], r[1], r[2], r[4]))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

# --------------------------
# GUI Design
# --------------------------
root = tk.Tk()
root.title("🛒 Billing System")
root.geometry("900x650")
root.config(bg="#E8F0FE")

# Fonts
title_font = ("Arial Rounded MT Bold", 18, "bold")
label_font = ("Segoe UI", 11)
button_font = ("Segoe UI", 10, "bold")

# Variables
customer_name = tk.StringVar()
item_name = tk.StringVar()
quantity = tk.StringVar()
item_price = tk.StringVar()
total_amount = tk.StringVar(value="0.00")

# --------------------------
# Header Frame
# --------------------------
header = tk.Frame(root, bg="#1565C0", height=70)
header.pack(fill="x")
tk.Label(header, text="🛒 Billing System", bg="#1565C0", fg="white", font=title_font).pack(pady=15)

# --------------------------
# Customer Info Frame
# --------------------------
cust_frame = tk.Frame(root, bg="#E8F0FE")
cust_frame.pack(pady=15)

tk.Label(cust_frame, text="Customer Name:", font=label_font, bg="#E8F0FE").grid(row=0, column=0, padx=10)
tk.Entry(cust_frame, textvariable=customer_name, width=30).grid(row=0, column=1)

# --------------------------
# Item Entry Frame
# --------------------------
item_frame = tk.Frame(root, bg="#E8F0FE")
item_frame.pack()

tk.Label(item_frame, text="Item Name:", bg="#E8F0FE", font=label_font).grid(row=0, column=0, padx=5)
tk.Entry(item_frame, textvariable=item_name, width=20).grid(row=0, column=1)

tk.Label(item_frame, text="Quantity:", bg="#E8F0FE", font=label_font).grid(row=0, column=2, padx=5)
tk.Entry(item_frame, textvariable=quantity, width=10).grid(row=0, column=3)

tk.Label(item_frame, text="Price:", bg="#E8F0FE", font=label_font).grid(row=0, column=4, padx=5)
tk.Entry(item_frame, textvariable=item_price, width=10).grid(row=0, column=5)

tk.Button(item_frame, text="➕ Add Item", command=add_item, bg="#2E7D32", fg="white",
          font=button_font, width=12, relief="ridge").grid(row=0, column=6, padx=10)

# --------------------------
# Bill Table Frame
# --------------------------
table_frame = tk.Frame(root, bg="#E8F0FE")
table_frame.pack(pady=15, fill="both", expand=True)

columns = ("Item", "Qty", "Price", "Total")
bill_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    bill_tree.heading(col, text=col)
bill_tree.pack(fill="both", expand=True, padx=20, pady=10)

# --------------------------
# Total & Buttons Frame
# --------------------------
bottom_frame = tk.Frame(root, bg="#E8F0FE")
bottom_frame.pack(pady=10)

# Total Box
total_box = tk.Frame(bottom_frame, bg="white", bd=2, relief="groove")
total_box.grid(row=0, column=0, padx=20)
tk.Label(total_box, text="Total Amount", bg="white", font=("Segoe UI", 12, "bold"), fg="#333").pack(padx=10, pady=(10, 0))
tk.Label(total_box, textvariable=total_amount, bg="white", fg="#00796B", font=("Arial", 14, "bold")).pack(padx=10, pady=(0, 10))

# Buttons
tk.Button(bottom_frame, text="💾 Generate Bill", command=generate_bill,
          bg="#1565C0", fg="white", font=button_font, width=15).grid(row=0, column=1, padx=10)
tk.Button(bottom_frame, text="📂 View Bills", command=show_bills,
          bg="#FB8C00", fg="white", font=button_font, width=15).grid(row=0, column=2, padx=10)
tk.Button(bottom_frame, text="🧹 Clear", command=clear_all,
          bg="#D32F2F", fg="white", font=button_font, width=12).grid(row=0, column=3, padx=10)

root.mainloop()