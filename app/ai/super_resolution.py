import cv2
from cv2 import dnn_superres

# Создаём sr-объект
async def img_sr(image):
	"""
	Улучшает качество изображения
	"""
	sr = dnn_superres.DnnSuperResImpl_create()

	# Считываем модель
	path = "app\\ai\\models\\FSRCNN_x4.pb"
	sr.readModel(path)

	# Устанавливаем модель и масштаб 
	sr.setModel("fsrcnn", 4)

	# Улучшаем
	result = sr.upsample(image)

	# Сохраняем
	return result