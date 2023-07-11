import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

url = "https://granite-expert.ru/info/materialy.html"

# Send a GET request to the page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the relevant content based on materials
cat_block2_divs = soup.find_all("div", class_="cat_block2")

# Create a directory to store the downloaded images
directory = "imgs"
if not os.path.exists(directory):
    os.makedirs(directory)

# Download and save the images
total_images = 0
base_url = "https://granite-expert.ru"
with tqdm(total=len(cat_block2_divs), desc="Downloading Images", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
    for div in cat_block2_divs:
        img_div = div.find("div", class_="cat_block_img2")
        if img_div is not None:
            img_tag = img_div.find("img")
            if img_tag is not None:
                image_url = urljoin(base_url, img_tag["src"])
                response = requests.get(image_url)
                if response.status_code == 200:
                    total_images += 1
                    image_name = img_tag.get("title", f"image_{total_images}")
                    image_path = os.path.join(directory, f"{image_name}.jpg")
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                pbar.update(1)
                pbar.set_postfix({"Total Images": total_images})

print("Download completed!")
print(f"Total images downloaded: {total_images}")
