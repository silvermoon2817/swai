import csv
product = []

class Shop:
    def __init__(self, name, category, price, sale, description):
        self.name = name
        self.category = category
        self.price = price
        self.sale = sale
        self.description = description

    def display_info(self):
        print(f"상품: {self.name}, 가격: {self.price}, 할인율: {self.sale}, 상세 설명: {self.description}")

def load_movies(filename):
    f = open(filename, "r", encoding = "utf-8-sig")
    reader = csv.reader(f)

    header = next(reader)
    print(header)

    for line in reader:
        name, category, price, sale, description = line
        object = Shop(name, category, price, sale, description)
        product.append(object)

    for m in product:
        m.display_info()

    f.close()
    
#인사하고
load_movies("product.csv")
#뭐 살지 물어보고
#할인율 계산
#장바구니 기능 추가