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
NUM_CLASSES = 7  # Задайте количество классов для классификации
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)  # Меняем последний слой на выход с нужным количеством классов
# model = model.to(device)

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
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Команда /start вызвана")
    await update.message.reply_text("Бот работает! Отправьте мне изображение.")


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

        response = f"Результат: класс {top_class.item()} с вероятностью {top_prob.item():.2f}"
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
