import cv2

def detect_objects(frame, cascade_classifier):
    """
    Функция для детекции объектов с использованием Haar Cascades.
    
    :param frame: Входное изображение (кадр).
    :param cascade_classifier: Загруженный классификатор Haar Cascade.
    :return: Кадр с наложенными прямоугольниками на обнаруженных объектах.
    """
    # Преобразование изображения в градации серого
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Обнаружение объектов
    objects = cascade_classifier.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Отрисовка прямоугольников вокруг обнаруженных объектов
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame

def main():
    # Путь к заранее обученному классификатору
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    
    # Загрузка классификатора Haar
    cascade_classifier = cv2.CascadeClassifier(cascade_path)
    if cascade_classifier.empty():
        print("Ошибка загрузки классификатора Haar Cascade.")
        return
    
    # Открываем камеру (0 — встроенная камера, можно указать путь к видеофайлу)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть камеру.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр.")
            break
        
        # Детекция объектов
        processed_frame = detect_objects(frame, cascade_classifier)
        
        # Показываем результат
        cv2.imshow("Haar Cascade Detection", processed_frame)

        # Нажмите 'q' для выхода
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
