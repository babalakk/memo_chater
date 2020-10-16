from django.conf import settings
from pymessenger.bot import Bot
bot = Bot(settings.FB_PAGE_TOKEN)


class Chater:
    def chat(recipient_id, text):
        bot.send_button_message(
            recipient_id=recipient_id,
            text="choose one",
            buttons=[
                {
                    "type": "postback",
                    "title": "return A",
                    "payload": "A"
                },                {
                    "type": "postback",
                    "title": "return B",
                    "payload": "B"
                }
            ])
