import csv
import re
import os


def get_data():
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [["Изготовитель системы",
                "Название ОС", "Код продукта", "Тип системы"]]

    for file in os.listdir('.\Chat\DZ2'):
        if file.startswith('info_') and file.endswith(".txt"):
            main_data.append([])
            with open(os.path.join('.\Chat\DZ2', file), 'r', encoding='cp1251') as f:

                for line in f:
                    os_prod = re.search(r"([иИ]зготовитель системы:)\s*(.*)", line)
                    if os_prod:
                        os_prod_list.append(os_prod.group(2).strip())

                    os_name = re.search(r"([нН]азвание ОС:)\s*(.*)", line)
                    if os_name:
                        os_name_list.append(os_name.group(2).strip())

                    os_code = re.search(r"([кК]од продукта:)\s*(.*)", line)
                    if os_code:
                        os_code_list.append(os_code.group(2).strip())

                    os_type = re.search(r"([тТ]ип системы:)\s*(.*)", line)
                    if os_type:
                        os_type_list.append(os_type.group(2).strip())

    for i, list in enumerate(main_data[1:]):
        list += [os_prod_list[i], os_name_list[i],
                os_code_list[i], os_type_list[i]]

    return main_data

def write_to_csv(file_path: str):
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f_writer = csv.writer(f)
        f_writer.writerows(get_data())

write_to_csv('.\Chat\DZ2\data.csv')