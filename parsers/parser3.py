import requests
import csv
import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

url = "https://granite-expert.ru/info/materialy.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

material_blocks = soup.find_all("div", class_="cat_block2")

data = []
total_materials = len(material_blocks)

progress_bar = tqdm(total=total_materials, desc="Progress", unit="material")


for block in material_blocks:
    material_name = block.find("a").text.strip()
    material_image_url = block.find("img")["src"].strip()
    
    # Collect additional information about the material
    material_url = "https://granite-expert.ru" + block.find("a")["href"]
    material_response = requests.get(material_url)
    material_soup = BeautifulSoup(material_response.content, "html.parser")
    
    material_info_div = material_soup.find("div", string="Информация о материале")
    if material_info_div is not None:
        material_info = material_info_div.find_next("div", class_="material_right_info_box")
        if material_info is not None:
            material_data = {
                "Название": material_name,
                "Страна": material_info.find("p", string="Страна:").find_next("span").text.strip(),
                "Цвет": material_info.find("p", string="Цвет:").find_next("span").text.strip(),
                "Тип": material_info.find("p", string="Тип:").find_next("span").text.strip(),
                "Структура": material_info.find("p", string="Структура:").find_next("span").text.strip(),
                "Плотность": material_info.find("p", string="Плотность:").find_next("span").text.strip(),
                "Изображение": material_image_url,
            }
            data.append(material_data)
            
            # Print the material data
            print("--------------------")
            print("Название:", material_data["Название"])
            print("Страна:", material_data["Страна"])
            print("Цвет:", material_data["Цвет"])
            print("Тип:", material_data["Тип"])
            print("Структура:", material_data["Структура"])
            print("Плотность:", material_data["Плотность"])
            print("Изображение:", material_data["Изображение"])
    
    progress_bar.update(1)
    progress_bar.set_postfix({"Material": material_name})

progress_bar.close()

# Save data to a text file
with open("materials_info.txt", "w", encoding="utf-8") as file:
    for material in data:
        file.write("--------------------\n")
        file.write(f"Название: {material['Название']}\n")
        file.write(f"Страна: {material['Страна']}\n")
        file.write(f"Цвет: {material['Цвет']}\n")
        file.write(f"Тип: {material['Тип']}\n")
        file.write(f"Структура: {material['Структура']}\n")
        file.write(f"Плотность: {material['Плотность']}\n")
        file.write(f"Изображение: {material['Изображение']}\n")

# Save data to a CSV file
csv_filename = "materials_info.csv"
csv_columns = ["Название", "Страна", "Цвет", "Тип", "Структура", "Плотность", "Изображение"]

with open(csv_filename, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(data)

# Save data to an Excel file
excel_filename = "materials_info.xlsx"
df = pd.DataFrame(data)
df.to_excel(excel_filename, index=False)

# Save data to a JSON file
json_filename = "materials_info.json"
with open(json_filename, "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

print("Parsing completed!")
print(f"Total materials parsed: {total_materials}")
print(f"Data saved to: {csv_filename}, {excel_filename}, {json_filename}, and materials_info.txt")
