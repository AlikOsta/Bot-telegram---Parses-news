import asyncio
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import telegram
import re
from telegram import Bot

load_dotenv()

# Функция для очистки имени файла
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Функция для парсинга HTML и получения информации о последней новости
def parse_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим блок с новостями
    blog_section = soup.find('div', class_='blog')
    if not blog_section:
        raise ValueError("Blog section not found")

    # Ищем первую новость
    latest_article = blog_section.find('article')
    if not latest_article:
        raise ValueError("Latest article not found")

    # Получаем заголовок новости
    title_tag = latest_article.find('h3', class_='cmsmasters_post_title entry-title')
    if not title_tag:
        raise ValueError("Title tag not found")
    title = title_tag.text.strip()

    # Получаем ссылку на статью
    link_tag = latest_article.find('a', class_='cmsmasters_img_link')
    if not link_tag:
        raise ValueError("Link tag not found")
    article_link = link_tag['href']

    # Получаем URL изображения
    img_tag = link_tag.find('img')
    if not img_tag:
        raise ValueError("Image tag not found in figure")
    image_url = img_tag['src']

    # Получаем текст статьи
    article_response = requests.get(article_link)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    content_tag = article_soup.find('div', class_='cmsmasters_post_content')
    if not content_tag:
        raise ValueError("Article content not found")
    paragraphs = content_tag.find_all('p')
    if len(paragraphs) >= 2:
        first_paragraph = paragraphs[0].text.strip()
        second_paragraph = paragraphs[1].text.strip()
        article_content = f"{first_paragraph}\n{second_paragraph}"
    else:
        article_content = paragraphs[0].text.strip()

    if not first_paragraph:
        raise ValueError("First paragraph not found")

    return title, article_content, image_url, article_link

# Функция для скачивания изображения и сохранения его с новым именем
async def download_image(image_url):
    post_id = image_url.split('/')[-1].split('.')[0]
    image_filename = f'img/{sanitize_filename(post_id)}.jpg'
    response = requests.get(image_url)
    with open(image_filename, 'wb') as f:
        f.write(response.content)
    return image_filename

# Функция для отправки сообщения в группу Telegram
async def send_message(bot, group_id, image_filename, message):
    async with bot:
        await bot.send_photo(chat_id=group_id, photo=open(image_filename, 'rb'), caption=message[:1000])

async def main():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    GROUP_ID = os.getenv('GROUP_ID')
    WEBSITE_URL = os.getenv('WEBSITE_URL')
    bot = telegram.Bot(token=TOKEN)

    while True:
        try:
            title, article_content, image_url, article_link = parse_website(WEBSITE_URL)

            if os.path.exists('last_post_id.txt'):
                with open('last_post_id.txt', 'r', encoding='utf-8') as f:
                    last_post_id = f.read().strip()
                if last_post_id == article_link:
                    await asyncio.sleep(850)
                    continue

            image_filename = await download_image(image_url)
            message = f"{title}\n\n{article_content}"
            await send_message(bot, GROUP_ID, image_filename, message)

            with open('last_post_id.txt', 'w', encoding='utf-8') as f:
                f.write(article_link)

            os.remove(image_filename)
            await asyncio.sleep(900)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(300)


asyncio.run(main())
