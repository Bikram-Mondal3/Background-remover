import os
import telebot
from rembg import remove
from PIL import Image
from io import BytesIO

BOT_TOKEN = os.environ.get('remover')  # Ensure the environment variable is set correctly

bot = telebot.TeleBot(BOT_TOKEN)

# Message handler that handles incoming /start, /hello, and /hi commands.
@bot.message_handler(commands=['start', 'hello', 'hi'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Nice to meet you. Is there anything I can assist you with?")

# Handling random Text Messages    
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, "I received your message: " + message.text)

def background_remover(image):
    try:
        output = remove(image)
        output_io = BytesIO()
        output.save(output_io, format='PNG')
        output_io.seek(0)
        return output_io
    except Exception as e:
        print(f"Error: {e}")
        return None

# Handling photos
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Nice photo! It will take a few moments to process...")

    # Fetching the photo file
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Open the photo from the downloaded file
    image = Image.open(BytesIO(downloaded_file))

    # Process the photo
    output_io = background_remover(image)

    if output_io:
        bot.send_photo(message.chat.id, output_io, caption="Here is your photo with the background removed!")
    else:
        bot.reply_to(message, "There was an error processing the photo.")

# Add the following to the end of your file to launch the bot
bot.infinity_polling()
