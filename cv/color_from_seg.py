import cv2
import numpy as np


IMAGE_PATH = ""

image = cv2.imread(IMAGE_PATH)

unique_colors = np.unique(image.reshape(-1, image.shape[2]), axis=0)

for i, color in enumerate(unique_colors):
    mask = cv2.inRange(image, color, color)

    segment_image = cv2.bitwise_and(image, image, mask=mask)

    output_path = f'segment_{i + 1}.png'
    cv2.imwrite(output_path, segment_image)

    print(f'Сегмент {i + 1} сохранен: {output_path}')


print("Найденные уникальные цвета сегментов:", unique_colors)
