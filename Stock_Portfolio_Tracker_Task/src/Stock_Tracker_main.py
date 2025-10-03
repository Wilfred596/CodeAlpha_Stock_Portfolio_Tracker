import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

# --- Hardcoded stock prices ---
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 320,
    "GOOG": 140
}

portfolio = {}
theme_mode = "Light"  # Default theme
SAVE_FILE = "portfolio.csv"
SETTINGS_FILE = "settings.txt"

# ------------------ Portfolio Functions ------------------
def add_stock():
    stock = stock_var.get()
    qty = qty_entry.get()

    if not stock:
        messagebox.showerror("Error", "Please select a stock.")
        return
    try:
        qty = int(qty)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    portfolio[stock] = portfolio.get(stock, 0) + qty
    update_table()
    save_portfolio_auto()
    qty_entry.delete(0, tk.END)

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    total_value = 0
    for stock, qty in portfolio.items():
        value = stock_prices[stock] * qty
        total_value += value
        tree.insert("", tk.END, values=(stock, qty, f"${stock_prices[stock]}", f"${value}"))
    total_label.config(text=f"💰 Total Investment: ${total_value}")

def save_portfolio_auto():
    with open(SAVE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock", "Quantity"])
        for stock, qty in portfolio.items():
            writer.writerow([stock, qty])

def load_portfolio_auto():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stock = row["Stock"]
                qty = int(row["Quantity"])
                if stock in stock_prices:
                    portfolio[stock] = qty
        update_table()

def save_portfolio_manual():
    if not portfolio:
        messagebox.showwarning("Warning", "Portfolio is empty.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
    if file_path:
        if file_path.endswith(".csv"):
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Stock", "Quantity", "Price", "Value"])
                total_value = 0
                for stock, qty in portfolio.items():
                    value = stock_prices[stock] * qty
                    total_value += value
                    writer.writerow([stock, qty, stock_prices[stock], value])
                writer.writerow(["TOTAL", "", "", total_value])
        else:
            with open(file_path, "w") as f:
                total_value = 0
                for stock, qty in portfolio.items():
                    value = stock_prices[stock] * qty
                    total_value += value
                    f.write(f"{stock}: {qty} × ${stock_prices[stock]} = ${value}\n")
                f.write(f"\nTotal Investment: ${total_value}\n")
        messagebox.showinfo("Saved", f"Portfolio saved to {file_path}")

# ------------------ Theme Functions ------------------
def toggle_theme():
    global theme_mode
    theme_mode = "Dark" if theme_mode == "Light" else "Light"
    apply_theme()
    save_settings()

def apply_theme():
    if theme_mode == "Light":
        bg_color = "#f4f6f8"
        fg_color = "black"
    else:
        bg_color = "#2c3e50"
        fg_color = "white"

    root.configure(bg=bg_color)
    input_frame.configure(bg=bg_color)
    btn_frame.configure(bg=bg_color)
    total_label.configure(bg=bg_color, fg=fg_color)

    for widget in input_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=bg_color, fg=fg_color)

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        f.write(theme_mode)

def load_settings():
    global theme_mode
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            theme_mode = f.read().strip()

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("📈 Simple Stock Tracker (Full Persistence)")
root.geometry("850x500")

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Stock Symbol:").grid(row=0, column=0, padx=5)
stock_var = tk.StringVar()
stock_dropdown = ttk.Combobox(input_frame, textvariable=stock_var, values=list(stock_prices.keys()), state="readonly")
stock_dropdown.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Quantity:").grid(row=0, column=2, padx=5)
qty_entry = tk.Entry(input_frame)
qty_entry.grid(row=0, column=3, padx=5)

tk.Button(input_frame, text="Add Stock", command=add_stock, bg="#4a90e2", fg="white").grid(row=0, column=4, padx=10)

# Table
columns = ("Stock", "Quantity", "Price", "Value")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)
tree.pack(pady=10)

# Total Label
total_label = tk.Label(root, text="💰 Total Investment: $0", font=("Arial", 12, "bold"))
total_label.pack()

# Buttons
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Save Portfolio As...", command=save_portfolio_manual, bg="#27ae60", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Toggle Theme", command=toggle_theme, bg="#8e44ad", fg="white").grid(row=0, column=1, padx=5)

# Load settings and portfolio before showing UI
load_settings()
apply_theme()
load_portfolio_auto()

root.mainloop()
