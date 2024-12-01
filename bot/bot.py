from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models
import logging

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

# Модель и трансформации
NUM_CLASSES = 7
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
weights_path = "cv/weights/classification/resnet18.pth"

try:
    checkpoint = torch.load(weights_path, map_location=torch.device("cpu"))
    state_dict = checkpoint.get("model_state_dict", checkpoint)
    model.load_state_dict(state_dict)
    print("Weights loaded successfully.")
except FileNotFoundError:
    print(f"Error: Weights file not found at {weights_path}.")
    exit()
except Exception as e:
    print(f"Error loading weights: {e}")
    exit()

model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Словарь классов
CLASS_NAMES = {
    1: "Convertible",
    2: "Coupe",
    3: "Hatchback",
    4: "Pick-Up",
    5: "SUV",
    6: "Sedan",
    7: "Van"
}

# Стандартные значения для классов
CLASS_STANDARD_VALUES = {
    "SUV": {
        "parts": {
            "hood": 2.0,
            "roof": 2.5,
            "fenders": 1.0,
            "front_doors": 2.2,
            "rear_doors": 1.8,
        },
        "paint_cost_per_m2": 500,
        "time_per_m2": 0.8,
    },
    "Sedan": {
        "parts": {
            "hood": 1.5,
            "roof": 2.0,
            "fenders": 0.8,
            "front_doors": 1.8,
            "rear_doors": 1.6,
        },
        "paint_cost_per_m2": 450,
        "time_per_m2": 0.7,
    },
    "Coupe": {
        "parts": {
            "hood": 1.4,
            "roof": 1.3,
            "fenders": 0.7,
            "front_doors": 2.0,
        },
        "paint_cost_per_m2": 480,
        "time_per_m2": 0.75,
    },
    "Hatchback": {
        "parts": {
            "hood": 1.2,
            "roof": 1.6,
            "fenders": 0.6,
            "front_doors": 1.6,
            "rear_doors": 1.2,
        },
        "paint_cost_per_m2": 460,
        "time_per_m2": 0.7,
    },
    "Convertible": {
        "parts": {
            "hood": 1.3,
            "roof": 1.0,
            "fenders": 0.7,
            "front_doors": 1.6,
        },
        "paint_cost_per_m2": 500,
        "time_per_m2": 0.8,
    },
    "Pick-Up": {
        "parts": {
            "hood": 1.8,
            "roof": 1.9,
            "fenders": 1.0,
            "front_doors": 2.1,
        },
        "paint_cost_per_m2": 550,
        "time_per_m2": 0.85,
    },
    "Van": {
        "parts": {
            "hood": 2.1,
            "roof": 3.0,
            "fenders": 1.2,
            "front_doors": 2.5,
            "rear_doors": 2.0,
        },
        "paint_cost_per_m2": 520,
        "time_per_m2": 0.9,
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Команда /start вызвана")
    await update.message.reply_text(
        "Бот работает! Отправьте изображение для классификации или текст с размером части, например: 'hood 1.5'."
    )


async def process_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info("Начата обработка изображения")
        file = await update.message.photo[-1].get_file()
        file_path = await file.download_to_drive()
        logger.info(f"Файл скачан: {file_path}")

        img = Image.open(file_path).convert("RGB")
        img_tensor = transform(img).unsqueeze(0)

        with torch.no_grad():
            output = model(img_tensor)

        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob, top_class = probabilities.topk(1)
        predicted_class = top_class.item() + 1  # Индексация начинается с 0

        # Получаем имя класса и стандартные значения
        class_name = CLASS_NAMES.get(predicted_class, "Unknown")
        standard_values = CLASS_STANDARD_VALUES.get(class_name, {})

        if not standard_values:
            await update.message.reply_text(f"Не удалось определить стандартные значения для класса {class_name}.")
            return

        parts = standard_values["parts"]
        paint_cost_per_m2 = standard_values["paint_cost_per_m2"]
        time_per_m2 = standard_values["time_per_m2"]

        # Рассчитываем стоимость и время для каждой части
        total_cost = 0
        total_time = 0
        part_details = []

        for part_name, area in parts.items():
            part_cost = area * paint_cost_per_m2
            part_time = area * time_per_m2
            total_cost += part_cost
            total_time += part_time
            part_details.append(f"{part_name.capitalize()} - {part_cost:.2f} рублей")

        # Формируем ответ
        response = (
            f"Результат: {class_name} с вероятностью {top_prob.item():.2f}\n\n"
            + "\n".join(part_details) +
            f"\n\nОбщая стоимость: {total_cost:.2f} рублей\n"
            f"Общее время: {total_time:.2f} часов"
        )

        logger.info(f"Ответ: {response}")
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Ошибка обработки изображения: {e}")
        await update.message.reply_text(f"Произошла ошибка: {e}")



def main():
    token = "7618094707:AAHgyzM6SCQvz-Iq-zifoAWxhQ93FrxL0f0"

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, process_image))

    application.run_polling()


if __name__ == "__main__":
    main()
