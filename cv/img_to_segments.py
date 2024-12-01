import cv2
import numpy as np
import os


def img_to_segments(img_path, img_hash, save_to_path):
    # Проверяем, существует ли директория для сохранения сегментов
    os.makedirs(save_to_path, exist_ok=True)

    # Загрузка изображения
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError(f"Не удалось загрузить изображение: {img_path}")

    # Размытие для уменьшения шумов
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Получение уникальных цветов
    rounded_image = (blurred_image // 10) * 10  # Округляем цвета с шагом 10
    unique_colors = np.unique(rounded_image.reshape(-1, rounded_image.shape[2]), axis=0)
    print(f"Уникальные цвета: {len(unique_colors)}")  # Лог количества уникальных цветов

    # Создание изображений для каждого сегмента
    segment_count = 0
    for i, color in enumerate(unique_colors):
        # Диапазон цвета с допуском
        lower_bound = np.clip(color - 10, 0, 255)
        upper_bound = np.clip(color + 10, 0, 255)

        # Создаем маску для текущего сегмента
        mask = cv2.inRange(blurred_image, lower_bound, upper_bound)

        # Проверка наличия сегмента
        if cv2.countNonZero(mask) == 0:
            continue

        # Создаем изображение только для этого сегмента
        segment_image = cv2.bitwise_and(image, image, mask=mask)

        # Сохранение результата
        output_path = os.path.join(save_to_path, f'segment_{segment_count + 1}.png')
        cv2.imwrite(output_path, segment_image)
        print(f"Сохранён сегмент {segment_count + 1}: {output_path}")
        segment_count += 1

    # Лог о завершении
    if segment_count == 0:
        print("Сегменты не найдены.")
    else:
        print(f"Всего выделено сегментов: {segment_count}")
