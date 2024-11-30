import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('masks/IMG_9208.png')

# Получение уникальных цветов (предполагается, что каждый сегмент имеет уникальный цвет)
unique_colors = np.unique(image.reshape(-1, image.shape[2]), axis=0)

# Создание изображений для каждого сегмента
for i, color in enumerate(unique_colors):
    # Создаем маску для текущего сегмента
    mask = cv2.inRange(image, color, color)

    # Создаем изображение только для этого сегмента
    segment_image = cv2.bitwise_and(image, image, mask=mask)

    # Сохранение результата
    output_path = f'/home/kirill/Projects/rosatom/segments/segment_{i + 1}.png'
    cv2.imwrite(output_path, segment_image)

    print(f'Сегмент {i + 1} сохранен: {output_path}')


# Опционально: показать уникальные цвета сегментов
print("Найденные уникальные цвета сегментов:", unique_colors)
