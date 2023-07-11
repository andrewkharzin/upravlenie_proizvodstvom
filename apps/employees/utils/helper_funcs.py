import os
import uuid
import datetime
from PIL import Image

def upload_empl_pic_to(instance, filename):
    # Генерация уникального имени файла
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    # Формирование пути сохранения файла
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    return f"photos/{year}/{month}/{day}/{filename}"


def create_thumbnail(image):
    # Открываем изображение
    img = Image.open(image.path)

    # Создаем превью с размером 100x100 пикселей
    thumb_size = (100, 100)
    img.thumbnail(thumb_size)

    # Определяем путь для сохранения превью
    thumb_path = f"{os.path.splitext(image.path)[0]}_thumb.jpg"

    # Сохраняем превью
    img.save(thumb_path)

    # Возвращаем путь к превью
    return thumb_path
