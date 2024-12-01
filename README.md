# Автопокраска

Проект для автоматического расчета стоимости и времени, необходимых для покраски различных частей автомобиля на основе изображения. 

## Основной функционал

- Распознавание класса автомобиля (sedan, SUV, van и т.д.) с использованием нейронной сети.
- Разделение изображения автомобиля на сегменты для выбора покраски отдельных частей.
- Расчет стоимости и человеко-часов для покраски каждой части на основе класса автомобиля и выбранных сегментов.
- Интеграция Telegram-бота для удобной отправки изображений и получения расчета стоимости.

## Архитектура проекта

![stack](screencast/stack.png)

### Фронтенд
- **Технологии**: [Tauri](https://tauri.app/) + [Svelte](https://svelte.dev/)
- **Функционал**:
1. Пользователь загружает изображение автомобиля.
2. Выбранное изображение обрабатывается и отображается с сегментами, которые пользователь может выбирать для покраски.
  
### Бэкенд
- **Технологии**: Flask
- **Обработка изображений**:
  - Классификация автомобиля: **ResNet50**
  - Сегментация изображения: **MAnet**
  - Используются библиотеки: PyTorch, OpenCV.
- **Логика расчета**:
  - После классификации автомобиль сопоставляется с данными из JSON-файла, содержащего размеры частей для каждого класса автомобилей.
  - Выбранные пользователем сегменты используются для расчета стоимости и человеко-часов.

### Telegram-бот
- Позволяет загружать изображения автомобилей и получать результаты классификации и расчета стоимости покраски.
- Использует ту же классификационную модель (**ResNet50**), что и основной сервис.

### Приложение
1. Загрузите изображение автомобиля.
2. Выберите нужные сегменты для покраски.
3. Получите расчет стоимости и времени на покраску.

### Telegram-бот
1. Отправьте изображение автомобиля боту.
2. Получите классификацию автомобиля.
3. Узнайте стоимость покраски каждой из частей.

## Будущие улучшения
- Добавление поддержки дополнительных классов автомобилей.
- Улучшение пользовательского интерфейса.
- Интеграция моделей для учета повреждений и сложностей покраски.
