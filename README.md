# Telegram News Bot

Бот для автоматической публикации новостей с сайта izvestia.ar в Telegram-канал.

## Возможности
- Парсинг новостей с сайта
- Извлечение заголовка, текста и изображений
- Автоматическая публикация в Telegram-канал
- Защита от дублирования постов
- Обработка ошибок и автоматическое восстановление

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
```
Windows:
```
python -m venv venv
.\venv\Scripts\activate
```
Linux/MacOS:
```
python -m venv venv
source venv/bin/activate
```
2. Установите зависимости:
```
pip install -r requirements.txt

```
3. Создайте файл .env и добавьте необходимые переменные:
```
TELEGRAM_TOKEN=ваш_токен
GROUP_ID=ваш_id_группы
WEBSITE_URL=https://izvestia.ar/
```
4. Запустите бота:
```
python bot-tg-news.py
```
#Cтруктура проекта
bot-tg-news.py - основной файл бота
requirements.txt - зависимости проекта
.env - конфигурационные переменные
img/ - временная папка для изображений

#Технологии
Python 3.8+
python-telegram-bot
BeautifulSoup4
requests
python-dotenv

Автор: Ostrovan Aleksei 
Telgram: @A43721
