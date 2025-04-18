import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters

# توكن البوت
TELEGRAM_API_TOKEN = '7396332921:AAG3bWZp7FMjLkMGxBbxYLMxPGCS0ZhbKyA'

# دالة لتحميل الفيديو باستخدام yt-dlp
def download_video(url: str, download_path: str):
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# دالة لمعالجة الرسائل في البوت
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('مرحبًا! أرسل لي رابط الفيديو لتحميله.')

async def handle_video_url(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    await update.message.reply_text('جاري تحميل الفيديو...')

    # تحميل الفيديو
    try:
        download_path = './downloads'
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        download_video(url, download_path)
        
        # إرسال الفيديو للمستخدم
        for filename in os.listdir(download_path):
            if filename.endswith('.mp4'):
                video_path = os.path.join(download_path, filename)
                await update.message.reply_video(video=open(video_path, 'rb'))
                os.remove(video_path)  # بعد إرسال الفيديو، يتم حذفه من المجلد
                break

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء تحميل الفيديو: {e}")

def main():
    # إنشاء Application باستخدام توكن البوت
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    
    # إضافة معالج لرسائل البداية
    application.add_handler(CommandHandler("start", start))
    
    # إضافة معالج للرسائل التي تحتوي على رابط
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_url))
    
    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
