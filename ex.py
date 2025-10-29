import tkinter as tk
from tkinter import messagebox
from tkinter import *
#import os
#import csv
#from PIL import Image, ImageTk

import csv
import os

product = []
cart = []
total = 0

class Shop:
    def __init__(self, name, category, price, sale, description, image_path=None):
        self.name = name
        self.category = category
        self.price = int(price)
        self.sale = float(sale)
        self.description = description
        self.image_path = image_path
        self.cart = []

    def sale_price(self):
        return int(self.price * (100 - self.sale)/100)

    def display_info(self):
        print(f"상품: {self.name}, 가격: {self.price}, 할인율: {self.sale}, 상세 설명: {self.description}")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("쇼핑몰")
        self.root.geometry("800x600")

        self.product = []
        self.cart = []
        self.current_frame = None
        
        self.load_product("product.csv")
        self.Pay_button()
        self.switch_frame(self.Display_category)

    def switch_frame(self, func):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        func(self.current_frame)

    def load_product(self, filename):
        with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            print(header)
            for line in reader:
                name, category, price, sale, description, image = line[:]
                obj = Shop(name, category, price, sale, description, image)
                self.product.append(obj)

    def Pay_button(self):
        pay_button = tk.Button(self.root, text="결제", command=self.total_price)
        pay_button.place(x=20, y=10)

    def total_price(self):
        if not self.cart:
            messagebox.showinfo("알림", "장바구니가 비어 있습니다.")
            return
        
        total = sum(item.sale_price() for item in self.cart)
        messagebox.showinfo("결제 완료", f"총 결제 금액: {total}원")
        self.cart.clear()

    def Display_category(self, frame):
        tk.Label(frame, text="카테고리 선택", font=("Arial", 20, "bold")).pack(pady=20)

        categories = sorted(set(p.category for p in self.product))

        if not categories:
            tk.Label(frame, text="상품이 없습니다.", fg="red").pack(pady=10)
            return

        for cate in categories:
            tk.Button(frame, text=cate, width=20,
                      command=lambda c=cate: self.switch_frame(lambda f: self.Display_products(f, c))
                      ).pack(pady=5)

    def Display_products(self, frame, category):
        tk.Label(frame, text=f"[{category}] 상품 목록", font=("Arial", 18)).pack(pady=20)
        filtered = [p for p in self.product if p.category == category]

        for p in filtered:
            button_text = f"{p.name} - {p.sale_price()}원 (할인 {int(p.sale*100)}%)"
            tk.Button(frame, text=button_text, width=40,
                      command=lambda prod=p: self.switch_frame(lambda f: self.Display_product_detail(f, prod, category))
                      ).pack(pady=4)
        tk.Button(frame, text="돌아가기", command=lambda: self.switch_frame(self.Display_category)).pack(pady=15)

    def Display_product_detail(self, frame, product, category):
        tk.Label(frame, text=f"{product.name}", font=("Arial", 18, "bold")).pack(pady=10)

        # 이미지 표시 (PIL 사용 시)
        # if product.image_path and os.path.exists(product.image_path):
        #     img = Image.open(product.image_path)
        #     img = img.resize((200, 200))
        #     photo = ImageTk.PhotoImage(img)
        #     img_label = tk.Label(frame, image=photo)
        #     img_label.image = photo
        #     img_label.pack(pady=5)
        # else:
        #     tk.Label(frame, text="[이미지를 찾을 수 없습니다]", fg="red").pack(pady=5)

        tk.Label(frame, text=f"가격: {product.price}원", font=("Arial", 12)).pack()
        tk.Label(frame, text=f"할인율: {int(product.sale*100)}%", font=("Arial", 12)).pack()
        tk.Label(frame, text=f"할인 적용가: {product.sale_price()}원", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(frame, text=f"상세 설명:\n{product.description}", wraplength=600, justify="left").pack(pady=10)

        tk.Button(frame, text="장바구니 추가", width=20, command=lambda: self.add_to_cart(product)).pack(pady=5)
        tk.Button(frame, text="뒤로가기", width=20,
                  command=lambda: self.switch_frame(lambda f: self.Display_products(f, category))).pack(pady=5)

    def add_to_cart(self, product):
        self.cart.append(product)
        messagebox.showinfo("장바구니", f"{product.name}이(가) 장바구니에 추가되었습니다.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
