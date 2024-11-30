import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import CommandStart
import asyncio
import requests
import base64
import json

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()         # Лог в консоль
    ]
)

users = dict()


# Функция для сохранения словаря
def save_users_to_file():
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


# Функция для загрузки словаря
def load_users_from_file():
    global users
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}


load_users_from_file()


def save_user(message):
    if str(message.from_user.id) not in users.keys():
        users[str(message.from_user.id)] = {None, None}
        save_users_to_file()


API_TOKEN = '7679663229:AAFKCcJZFxk7gecKA0QQS_ZBMT5nC2Kn91M'
BACKEND_URL = 'http://127.0.0.1:5000'   # Подставить нужный адрес

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Загружает изображение на Backend
async def upload_image_to_backend(image_data):
    logging.info("Загрузка изображения на Backend...")
    base64_image = base64.b64encode(image_data).decode('utf-8')
    try:
        response = requests.post(
            f"{BACKEND_URL}/",
            json={"image": base64_image}
        )
        logging.info("Изображение успешно отправлено на Backend.")
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка при отправке изображения на Backend: {e}")
        return {"error": str(e)}


# Проверяет статус обработки
def check_status(image_hash):
    logging.info(f"Проверка статуса обработки для ID: {image_hash}")
    try:
        response = requests.get(f"{BACKEND_URL}/{image_hash}/status")
        logging.info(f"Статус для ID {image_hash}: {response.json().get('status', 'Неизвестно')}")
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка при проверке статуса: {e}")
        return {"status": "Error"}


# Получает сегменты
def get_segments(image_hash):
    logging.info(f"Получение сегментов для ID: {image_hash}")
    try:
        response = requests.get(f"{BACKEND_URL}/{image_hash}/segments")
        logging.info(f"Сегменты для ID {image_hash}: {response.json()}")
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка при получении сегментов: {e}")
        return {"error": str(e)}


# Обработчик команды /start
@dp.message(CommandStart())
async def start_command(message: types.Message):
    logging.info("Получена команда /start.")
    await message.reply("Привет! Отправь мне фото машины, и я рассчитаю стоимость покраски. Но сначала отправь мне "
                        "технические данные по покраске.")


# Обработчик фото
@dp.message(lambda message: message.content_type == ContentType.PHOTO)
async def handle_photo(message: types.Message):
    logging.info(f"Получено фото от пользователя {message.from_user.id}")
    await message.reply("Получил фото. Начинаю обработку...")

    # Получаем файл ID
    photo = message.photo[-1]
    try:
        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path
        logging.info(f"Файл фото загружен. Путь: {file_path}")

        # Скачиваем файл
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"
        response = requests.get(file_url)
        image_data = response.content
        logging.info("Фото успешно скачано.")

        # Отправляем изображение на Backend
        backend_response = await upload_image_to_backend(image_data)

        if 'error' in backend_response:
            logging.error(f"Ошибка при загрузке на Backend: {backend_response['error']}")
            await message.reply(f"Ошибка загрузки: {backend_response['error']}")
            return

        image_hash = backend_response['image_hash']
        logging.info(f"Фото успешно отправлено на Backend. ID: {image_hash}")
        await message.reply(f"Фото отправлено на обработку. ID: {image_hash}. Проверяю статус...")

        # Ждём завершения обработки
        while True:
            status_response = check_status(image_hash)
            if status_response['status'] == 'Ready':
                logging.info(f"Обработка завершена для ID: {image_hash}")
                break
            elif status_response['status'] == 'Error':
                logging.error(f"Ошибка обработки для ID: {image_hash}")
                await message.reply("Произошла ошибка при обработке.")
                return
            await asyncio.sleep(2)

        # Получаем сегменты
        segments_response = get_segments(image_hash)
        if 'error' in segments_response:
            logging.error(f"Ошибка получения сегментов: {segments_response['error']}")
            await message.reply(f"Ошибка получения сегментов: {segments_response['error']}")
        else:
            segments = segments_response['segments']
            logging.info(f"Обработка завершена. Сегменты: {segments}")
            await message.reply(f"Обработка завершена! Сегменты: {segments}")
    except Exception as e:
        logging.error(f"Ошибка при обработке фото: {e}")
        await message.reply("Произошла ошибка при обработке фото.")

if __name__ == '__main__':
    logging.info("Бот запущен.")
    asyncio.run(dp.start_polling(bot))
