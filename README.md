# Шаблоны программ для хакатона


## Структура проекта

- `/templates/cv` — примеры работы с изображениями и видео для задач компьютерного зрения.

## Backend

### How to run

1. Install Python
Ensure that Python 3.6+ is installed on your machine. You can download and install it from python.org.
2. Install Required Libraries
The script requires Flask, base64, asyncio, and hashlib. These libraries should be installed in your Python environment.

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```

4. Running the Flask App

To start the Flask application, open a terminal or command prompt, navigate to the folder where the script is saved, and run the following command:
```bash
python backend.py
```


### Endpoints

- POST "/" - загрузка изображения и начало обработки
- GET "/" - возвращает все созданные идентификаторы
- GET "/<id>/status" - статус обработки
- GET "/<id>/segments" - сегменты изображения

