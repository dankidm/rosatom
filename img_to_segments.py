import cv2
import numpy as np
import os


def img_to_segments(img_path, img_hash, save_to_path):
    # Загрузка изображения
    image = cv2.imread(img_path)

    # Получение уникальных цветов (предполагается, что каждый сегмент имеет уникальный цвет)
    unique_colors = np.unique(image.reshape(-1, image.shape[2]), axis=0)
    # Создание изображений для каждого сегмента
    for i, color in enumerate(unique_colors):
        # Создаем маску для текущего сегмента
        mask = cv2.inRange(image, color, color)

        # Создаем изображение только для этого сегмента
        segment_image = cv2.bitwise_and(image, image, mask=mask)

        # Сохранение результата
        output_path = f'{save_to_path}/segment_{i + 1}.png'
        cv2.imwrite(output_path, segment_image)
