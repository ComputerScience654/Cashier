import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# เมนูอาหารและราคา
menu_items = {
    "ข้าวมันไก่": 50,
    "ก๋วยเตี๋ยว": 40,
    "ข้าวผัด": 45,
    "น้ำเปล่า": 10,
    "น้ำอัดลม": 20
}

cart = {}
VAT_RATE = 0.15

def add_to_cart(item):
    if item in cart:
        cart[item] += 1
    else:
        cart[item] = 1
    update_cart_display()

def clear_cart():
    global cart
    cart.clear()
    update_cart_display()

def update_cart_display():
    cart_text.config(state=tk.NORMAL)
    cart_text.delete(1.0, tk.END)

    if not cart:
        cart_text.insert(tk.END, "ตะกร้าว่าง\n")
    else:
        total = sum(menu_items[item] * qty for item, qty in cart.items())
        vat = total * VAT_RATE
        grand_total = total + vat

        for item, qty in cart.items():
            cart_text.insert(tk.END, f"{item} x{qty} = {menu_items[item] * qty} บาท\n")

        cart_text.insert(tk.END, f"\nราคารวม: {total} บาท")
        cart_text.insert(tk.END, f"\nVAT (15%): {vat:.2f} บาท")
        cart_text.insert(tk.END, f"\nราคาสุทธิ: {grand_total:.2f} บาท")

    cart_text.config(state=tk.DISABLED)

def checkout():
    if not cart:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกสินค้าอย่างน้อยหนึ่งรายการ")
        return
    
    confirm = messagebox.askyesno("ยืนยันการชำระเงิน", "คุณต้องการชำระเงินหรือไม่?")
    if not confirm:
        return

    receipt_window = tk.Toplevel(root)
    receipt_window.title("ใบเสร็จ")
    receipt_window.geometry("400x500")

    try:
        image = Image.open("C:/procash/logo.png")
        image = image.resize((50, 50), Image.LANCZOS)
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(receipt_window, image=logo)
        logo_label.image = logo
        logo_label.pack()
    except Exception as e:
        print(f"Error loading logo: {e}")

    receipt_text = tk.Text(receipt_window, height=20)
    receipt_text.pack(fill=tk.BOTH, expand=True)
    receipt_text.insert(tk.END, "=== ใบเสร็จ ===\n\n")

    total = sum(menu_items[item] * qty for item, qty in cart.items())
    vat = total * VAT_RATE
    grand_total = total + vat

    for item, qty in cart.items():
        price = menu_items[item] * qty
        receipt_text.insert(tk.END, f"{item} x{qty} = {price} บาท\n")

    receipt_text.insert(tk.END, f"\nราคารวม: {total} บาท")
    receipt_text.insert(tk.END, f"\nVAT (15%): {vat:.2f} บาท")
    receipt_text.insert(tk.END, f"\nราคาสุทธิ: {grand_total:.2f} บาท")

    receipt_text.config(state=tk.DISABLED)

    cart.clear()
    update_cart_display()

# สร้าง GUI หลัก
root = tk.Tk()
root.title("โปรแกรมแคชเชียร์")
root.geometry("500x700")
root.configure(bg="#f8f8f8")

# ==== Section: เมนูอาหาร ====
menu_frame = tk.LabelFrame(root, text="เมนูอาหาร", font=("Arial", 14, "bold"), padx=10, pady=10, bg="white")
menu_frame.pack(padx=20, pady=10, fill="both")

row, col = 0, 0
for item, price in menu_items.items():
    btn = tk.Button(menu_frame, text=f"{item}\n({price} บาท)", font=("Arial", 12), width=15, height=2,
                    bg="#ffcc99", command=lambda i=item: add_to_cart(i))
    btn.grid(row=row, column=col, padx=10, pady=5)
    
    col += 1
    if col > 1:  # จัดเรียงเป็น 2 คอลัมน์
        col = 0
        row += 1

# ==== Section: ตะกร้าสินค้า ====
cart_frame = tk.LabelFrame(root, text="ตะกร้าสินค้า", font=("Arial", 14, "bold"), padx=10, pady=10, bg="white")
cart_frame.pack(padx=20, pady=10, fill="both", expand=True)

cart_text = tk.Text(cart_frame, height=10, font=("Arial", 12), bg="#fff9e6")
cart_text.pack(fill=tk.BOTH, expand=True)

# ==== Section: ปุ่มชำระเงิน & ล้างตะกร้า ====
button_frame = tk.Frame(root, bg="#f8f8f8")
button_frame.pack(padx=20, pady=10, fill="both")

checkout_btn = tk.Button(button_frame, text="ชำระเงิน", font=("Arial", 14, "bold"), fg="white", bg="#4CAF50", height=2, command=checkout)
checkout_btn.pack(side=tk.LEFT, expand=True, fill="both", padx=5)

clear_btn = tk.Button(button_frame, text="ล้างตะกร้า", font=("Arial", 14, "bold"), fg="white", bg="#f44336", height=2, command=clear_cart)
clear_btn.pack(side=tk.RIGHT, expand=True, fill="both", padx=5)

root.mainloop()
