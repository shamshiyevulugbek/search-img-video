import logging
from googletrans import Translator
import requests

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5266254215:AAGPQEQs2p5mp-5lMbbnKl91RLYcT9hfLGo'
url_img = "https://pixabay.com/api/"
url_video ="https://pixabay.com/api/videos/"
api_key = "26235096-f05bfbebacf7a814c40534664"
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(xabar: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await xabar.reply("Assalom alaykum!\nVideo va rasmlarni qisqa muddatda toping😃")
    
@dp.message_handler()
async def echo(salom: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    if salom.text.startswith("img/") or salom.text.startswith("video/"):
        translator = Translator()
        if salom.text.startswith("img/"):
            my_text = salom.text[4:]
            img_text = translator.translate(my_text).text
            params = {'key':api_key,'q':img_text}
            r = requests.get(url_img,params=params)
            try:
                img_url = r.json()['hits'][0]["largeImageURL"]
                await salom.answer_photo(img_url)
            except:
                await salom.reply("👉Bunday rasmli ma'lumot topilmadi 🙅")
        else:
            my_text = salom.text[6:]
            video_text = translator.translate(my_text).text
            params = {'key':api_key,'q':video_text}
            r = requests.get(url_video,params=params)
            try:
                video_url = r.json()['hits'][0]['videos']['medium']['url']
                await salom.answer_video(video_url)
            except:
                await salom.reply("👉Bunday videoli ma'lumot topilmadi 🙅")
    else:
        await salom.reply("👉Video qidirish uchun \"video/video_name\"\n👉Rasm qidirish uchun \"img/img_name\" ko'rinishida kiriting!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)