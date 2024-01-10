import telebot
from pytube import YouTube
import os

BOT_TOKEN = '6651176548:AAF3ilQESTzq2_7MyhGacexXJIySCYRCs64'

bot = telebot.TeleBot(BOT_TOKEN) 

print("Bot started!")

@bot.message_handler(commands=['start'])
def send_welcome(pm):
    bot.reply_to(pm, "Welcome to YouTube to mp3 converter made by Sangeet!\nEnter the link to the video that you want to convert.")
    bot.register_next_step_handler(pm, download_handler)

def download_handler(pm):
    url = pm.text
    sent_msg = bot.send_message(pm.chat.id, "Download started. Please wait!")
    yt = YouTube(url)
    stream = yt.streams.get_audio_only()
    stream.download()
    file_name = stream.title.replace(' ', '-')
    os.rename(f"{stream.title}.mp4", f"{file_name}.mp4")
    with open(f'{file_name}.mp4', 'rb') as file:
        bot.send_audio(pm.chat.id, file, timeout=10000)
    bot.send_message(pm.chat.id, "Download finished!\nEnjoy your music :)")
    os.remove(f"{file_name}.mp4")

bot.infinity_polling()