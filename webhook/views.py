import hashlib
import hmac
import http.client
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.
def handle_webhook(event, payload):
    print('Received the {} event'.format(event))
    print(json.dumps(payload, indent=4))

@csrf_exempt
def handle_github_hook(request):
    print(request)
    # Check the X-Hub_signature header to make sure this is a valid request
    github_signature = request.META['HTTP_X_HUB_SIGNATURE']
    signature = hmac.new(settings.GITHUB_WEBHOOK_SECRET, request.body, hashlib.sha1)
    expected_signature = 'sha1=' + signature.hexdigets()
    if not hmac.compare_digest(github_signature, expected_signature):
        return HttpResponseForbidden('Invalid signature header')

    if 'payload' in request.POST:
       payload = json.loads(request.POST['payload'])
    else:
        payload = json.loads(request.body)

    event = request.META['HTTP_X_GITHUB_EVENT']

    handle_webhook(event, payload)

    return HttpResponseForbidden('Webhook received', status=http.client.ACCEPTED)