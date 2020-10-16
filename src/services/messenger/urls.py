from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.chater.client import Chater
import json
import traceback


def is_postback(data):
    return data.get("entry")[0].get("messaging")[0].get("postback") is not None


@csrf_exempt
def root(request):
    try:
        if request.method == "GET":
            return HttpResponse(request.GET["hub.challenge"])
        elif request.method == "POST":
            data = json.loads(request.body)
            recipient_id = data.get("entry")[0].get("messaging")[0].get("sender").get("id")
            if is_postback(data):
                text = data.get("entry")[0].get("messaging")[0].get("postback").get("payload")
            else:
                text = data.get("entry")[0].get("messaging")[0].get("message").get("text")
            if recipient_id and text:
                Chater.chat(recipient_id=recipient_id, text=text)
    except Exception as e:
        traceback.print_exc()
    return HttpResponse("OK")


urlpatterns = [
    path('', root),
]
