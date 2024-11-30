import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from segmentation_models_pytorch import MAnet
import numpy as np


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


ENCODER = "resnet34"  # Должен соответствовать энкодеру, для которого были сохранены веса
CLASSES = 22  # Количество классов сегментации (включая фон)
ACTIVATION = "sigmoid"  # Активация на выходе

# Создание модели
model = MAnet(
    # encoder_name=ENCODER,
    # encoder_weights=None,  # Предобученные веса не загружаем здесь
    classes=CLASSES,
    # activation=ACTIVATION
)

# Путь к файлу с весами
weights_path = "weights/model_weights.pth"

# Загрузка весов
try:
    checkpoint = torch.load(weights_path, map_location=torch.device("cpu"))
    
    # Если файл содержит дополнительные ключи, такие как "model_state_dict"
    if "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]  # Извлекаем только параметры модели
    else:
        state_dict = checkpoint  # Если файл содержит только state_dict

    # Загрузка весов в модель
    model.load_state_dict(state_dict)
    print("Weights loaded successfully.")
except FileNotFoundError:
    print(f"Error: Weights file not found at {weights_path}.")
    exit()
except Exception as e:
    print(f"Error loading weights: {e}")
    exit()

# Переключение модели в режим оценки
model.eval()

def load_image(image_path, transform=None):
    image = Image.open(image_path).convert("RGB")
    if transform:
        image = transform(image)
    return image

transform = transforms.Compose([
    transforms.Resize((320, 320)),  # Изменение размера
    transforms.ToTensor(),          # В тензор
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Нормализация
])

image_path = "Car damages 1054.png" 
input_image = load_image(image_path , transform=transform)
print(type(input_image))
input_image = input_image.unsqueeze(0).to(device)  

def save_multiclass_segmentation(output, output_path, num_classes=22):
    """
    Сохраняет многоклассовую сегментацию с уникальными цветами для каждого класса.

    :param output: Сегментированная маска (numpy array), значения в диапазоне [0, num_classes).
    :param output_path: Путь для сохранения результата.
    :param num_classes: Общее количество классов.
    """
    # Определяем цвета для классов
    np.random.seed(42)  # Для детерминированности
    class_colors = np.random.randint(0, 255, size=(num_classes, 3), dtype=np.uint8)

    # Создаём цветную маску
    height, width = output.shape
    mask = np.zeros((height, width, 3), dtype=np.uint8)

    for cls in range(num_classes):
        mask[output == cls] = class_colors[cls]

    # Сохранение результата
    segmented_image = Image.fromarray(mask)
    segmented_image.save(output_path)
    print(f"Segmented image saved to {output_path}")

# Пример использования
with torch.no_grad():
    output = model(input_image)
    output = torch.argmax(output, dim=1).squeeze().cpu().numpy()  # Получаем классы для каждого пикселя

save_multiclass_segmentation(output, "segmented_image.png", num_classes=22)

