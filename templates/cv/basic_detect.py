import cv2
import numpy as np

def detect_objects(frame, lower_color, upper_color):
    """
    Функция для детекции объектов по цвету.
    
    :param frame: Входное изображение (кадр с камеры или видео).
    :param lower_color: Нижняя граница HSV-диапазона.
    :param upper_color: Верхняя граница HSV-диапазона.
    :return: Обработанное изображение с наложенными контурами.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame, mask

def main():
    cap = cv2.VideoCapture(0)

    lower_color = np.array([100, 150, 50])  
    upper_color = np.array([140, 255, 255])

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр.")
            break

        processed_frame, mask = detect_objects(frame, lower_color, upper_color)

        cv2.imshow("Original Frame", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Processed Frame", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
