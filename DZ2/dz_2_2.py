import json

def write_to_json(item: str, quantity: int, price: float, buyer: str, date: str):
    data = {"orders": [{"item": item}, {"quantity": quantity}, {"price": price}, {"buyer": buyer}, {"date": date}]}

    with open(".\chat\DZ2\orders.json", "w") as f:
        json.dump(data, f, indent=4)

write_to_json("Bike", 1, 20000, "Wick J.", "13.10.2022")