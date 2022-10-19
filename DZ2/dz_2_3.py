import yaml

data = {"1\u20ac": ["one", "two", "three"], "2\u20ac": 2, "3\u20ac": {"Firstname": "John", "Lasname": "Wick"}}

with open(".\chat\DZ2\data.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

with open(".\chat\DZ2\data.yaml", "r", encoding="utf-8") as f:
    f_reader = yaml.load(f, Loader=yaml.loader.Loader)
    print(f_reader)