from django.conf import settings
from pymessenger.bot import Bot
bot = Bot(settings.FB_PAGE_TOKEN)


class Chater:
    def chat(recipient_id, text):
        bot.send_text_message(recipient_id=recipient_id, message=text)
