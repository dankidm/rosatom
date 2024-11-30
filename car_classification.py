import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

NUM_CLASSES = 7  # Задайте количество классов для классификации
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)  # Меняем последний слой на выход с нужным количеством классов
model = model.to(device)

weights_path = "weights/classification/resnet18.pth"

try:
    checkpoint = torch.load(weights_path, map_location=torch.device("cpu"))

    if "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
    else:
        state_dict = checkpoint

    model.load_state_dict(state_dict)
    print("Weights loaded successfully.")
except FileNotFoundError:
    print(f"Error: Weights file not found at {weights_path}.")
    exit()
except Exception as e:
    print(f"Error loading weights: {e}")
    exit()

model.eval()


def load_image(image_path, transform=None):
    image = Image.open(image_path).convert("RGB")
    if transform:
        image = transform(image)
    return image


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def get_car_type(image_path):
    input_image = load_image(image_path, transform=transform)
    input_image = input_image.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_image)
        predicted_class = torch.argmax(output, dim=1).item()
        return predicted_class
