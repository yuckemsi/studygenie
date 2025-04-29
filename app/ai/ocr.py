import cv2
import pytesseract
import numpy as np
from app.ai.super_resolution import img_sr

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

async def text_recognize(image_bytes):
    """
    Распознает текст из изображения, переданного в виде байтового объекта.
    """
    # Преобразуем байты в массив numpy
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Применяем суперразрешение (если нужно)
    img = await img_sr(img)

    # Преобразуем изображение в RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Конфигурация для Tesseract
    config = r'--oem 3 --psm 6'
    res = pytesseract.image_to_string(img, lang='rus+eng', config=config)
    
    return res