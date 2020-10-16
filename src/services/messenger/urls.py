from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.chater.client import Chater
import json


@csrf_exempt
def root(request):
    if request.method == "GET":
        return HttpResponse(request.GET["hub.challenge"])
    elif request.method == "POST":
        data = json.loads(request.body)
        recipient_id = data.get("entry")[0].get("messaging")[0].get("sender").get("id")
        text = data.get("entry")[0].get("messaging")[0].get("message").get("text")
        Chater.chat(recipient_id=recipient_id, text=text)
    return HttpResponse("OK")


urlpatterns = [
    path('', root),
]
