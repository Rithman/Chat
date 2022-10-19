import json


def write_to_json(item: str, quantity: int, price: float, buyer: str, date: str):
    with open(".\chat\DZ2\orders.json", "r", encoding='utf-8') as f_out:
        data_out = json.load(f_out)
    with open(".\chat\DZ2\orders.json", "w", encoding='utf-8') as f_in:
        data_in = {"item": item, "quantity": quantity,
                   "price": price, "buyer": buyer, "date": date}
        data_out["orders"].append(data_in)
        json.dump(data_out, f_in, ensure_ascii=False, indent=2)


write_to_json("Bike", 1, 20000, "Wick J.", "13.10.2022")
write_to_json("Мотоцикл", 1, 50000, "Иванов. А.В", "13.10.2022")
