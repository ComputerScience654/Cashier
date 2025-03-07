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

def update_cart_display():
    cart_text.delete(1.0, tk.END)
    total = 0
    for item, qty in cart.items():
        price = menu_items[item] * qty
        cart_text.insert(tk.END, f"{item} x{qty} = {price} บาท\n")
        total += price
    vat = total * VAT_RATE
    grand_total = total + vat
    cart_text.insert(tk.END, f"\nราคารวม: {total} บาท")
    cart_text.insert(tk.END, f"\nVAT (15%): {vat:.2f} บาท")
    cart_text.insert(tk.END, f"\nราคาสุทธิ: {grand_total:.2f} บาท")

def checkout():
    if not cart:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกสินค้าอย่างน้อยหนึ่งรายการ")
        return

    # สร้างหน้าต่างใหม่สำหรับใบเสร็จ
    receipt_window = tk.Toplevel(root)
    receipt_window.title("ใบเสร็จ")
    receipt_window.geometry("400x500")

    # เพิ่มโลโก้
    try:
        image = Image.open("C:/procash/logo.png")
        image = image.resize((50, 50), Image.LANCZOS)  # ปรับขนาดโลโก้ที่นี่
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(receipt_window, image=logo)
        logo_label.image = logo  # เก็บ reference ของโลโก้
        logo_label.pack()
    except Exception as e:
        messagebox.showerror("Error", f"ไม่สามารถโหลดโลโก้ได้: {e}")

    # แสดงใบเสร็จ
    receipt_text = tk.Text(receipt_window, height=20)
    receipt_text.pack(fill=tk.BOTH, expand=True)
    receipt_text.insert(tk.END, "=== ใบเสร็จ ===\n\n")

    # แก้ไขส่วนนี้ เพื่อแสดงรายการสินค้าในใบเสร็จ
    total = 0
    for item, qty in cart.items():
        price = menu_items[item] * qty
        receipt_text.insert(tk.END, f"{item} x{qty} = {price} บาท\n")
        total += price
    vat = total * VAT_RATE
    grand_total = total + vat
    receipt_text.insert(tk.END, f"\nราคารวม: {total} บาท")
    receipt_text.insert(tk.END, f"\nVAT (15%): {vat:.2f} บาท")
    receipt_text.insert(tk.END, f"\nราคาสุทธิ: {grand_total:.2f} บาท")

    receipt_text.config(state=tk.DISABLED)  # ป้องกันการแก้ไข

    # เคลียร์ตะกร้า
    cart.clear()
    update_cart_display()

# GUI
root = tk.Tk()
root.title("โปรแกรมแคชเชียร์")
root.geometry("500x600")

# ปุ่มเมนู
for item, price in menu_items.items():
    btn = tk.Button(root, text=f"{item} ({price} บาท)", command=lambda i=item: add_to_cart(i))
    btn.pack(fill=tk.X, padx=40, pady=10)  # กำหนด padding แทนการใช้ width และ height

# แสดงตะกร้าสินค้า
cart_text = tk.Text(root, height=10)
cart_text.pack(fill=tk.BOTH, expand=True)

# ปุ่มชำระเงิน
checkout_btn = tk.Button(root, text="ชำระเงิน", command=checkout)
checkout_btn.pack(fill=tk.X)

root.mainloop()
